"""Course helper — returns a ready google-genai client, whichever Google endpoint your key belongs to.

Why this exists: a Google API key can belong to two different worlds —
the Vertex / Agent Platform (Path A in Block 0) or the Gemini Developer API
(Path B). The client must be told which; guessing wrong gives a scary 403.
This helper tries both once, remembers the answer in ~/.course_env, and
hands you a working client. Use it everywhere:

    import course_utils
    client = course_utils.get_client()
    r = client.models.generate_content(model=course_utils.MODEL, contents="...")
"""

import os
import pathlib

_ENV_FILE = pathlib.Path.home() / ".course_env"


def _load_env():
    if _ENV_FILE.exists():
        for line in _ENV_FILE.read_text().splitlines():
            if line.startswith("export ") and "=" in line:
                k, v = line[len("export "):].split("=", 1)
                os.environ.setdefault(k, v.strip().strip('"'))


_load_env()

# The course default. On paid / Vertex-trial credit you may upgrade, e.g.:
#   echo 'export COURSE_MODEL="gemini-3.5-flash"' >> ~/.course_env
# then restart your notebook kernel / app. Report the exact model string in
# your AI-use log — the model is your instrument.
MODEL = os.environ.get("COURSE_MODEL", "gemini-2.5-flash")


def _persist(key, value):
    """Set (value=str) or remove (value=None) an export line in ~/.course_env."""
    lines = []
    if _ENV_FILE.exists():
        lines = [l for l in _ENV_FILE.read_text().splitlines() if not l.startswith(f'export {key}=')]
    if value is not None:
        lines.append(f'export {key}="{value}"')
    _ENV_FILE.write_text("\n".join(lines) + "\n")
    _ENV_FILE.chmod(0o600)


def _configure_gemini_cli(mode, key):
    """Write Gemini CLI's own config (~/.gemini/.env + settings.json) so the
    `gemini` command works in every terminal with no shell setup and no
    sign-in dialog. Called automatically after every successful API check —
    so this heals itself even if a student deletes the files."""
    try:
        import json
        gem_dir = pathlib.Path.home() / ".gemini"
        gem_dir.mkdir(exist_ok=True)
        env_lines = [f'GEMINI_API_KEY="{key}"', f'GOOGLE_API_KEY="{key}"']
        if mode == "vertex":
            env_lines.append("GOOGLE_GENAI_USE_VERTEXAI=true")
        env_file = gem_dir / ".env"
        env_file.write_text("\n".join(env_lines) + "\n")
        env_file.chmod(0o600)
        sfile = gem_dir / "settings.json"
        try:
            settings = json.loads(sfile.read_text()) if sfile.exists() else {}
        except Exception:
            settings = {}
        settings["selectedAuthType"] = "vertex-ai" if mode == "vertex" else "gemini-api-key"
        sfile.write_text(json.dumps(settings, indent=2))
    except Exception:
        pass  # CLI convenience must never break the API path


def get_client(verbose=False):
    """A working genai client, or a RuntimeError that tells you what to do."""
    _load_env()
    key = os.environ.get("GEMINI_API_KEY")
    os.environ.pop("GOOGLE_API_KEY", None)  # silence SDK dual-key warning; CLI reads it from files
    if not key:
        raise RuntimeError("No API key stored yet — run: bash check_setup.sh")

    from google import genai

    known = os.environ.get("GEMINI_MODE")

    # Fast path: if a previous run already verified which endpoint this key
    # belongs to, build the client without spending a test request on it.
    # (check_setup.sh and any failed real call still exercise the full path.)
    if known in ("vertex", "dev") and not verbose:
        _configure_gemini_cli(known, key)
        return genai.Client(vertexai=(known == "vertex"), api_key=key)

    if known in ("vertex", "dev"):
        candidates = [known, "dev" if known == "vertex" else "vertex"]
    else:
        candidates = ["vertex", "dev"]
    errors = []
    for mode in candidates:
        try:
            client = genai.Client(vertexai=(mode == "vertex"), api_key=key)
            client.models.generate_content(model=MODEL, contents="ping")
            if mode != known:
                _persist("GEMINI_MODE", mode)
            # The gemini CLI needs one extra breadcrumb for Vertex keys —
            # and must NOT have it for Developer-API keys. Keep it in sync
            # every time, so older setups self-repair:
            if mode == "vertex":
                _persist("GOOGLE_GENAI_USE_VERTEXAI", "true")
                os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
            else:
                _persist("GOOGLE_GENAI_USE_VERTEXAI", None)
                os.environ.pop("GOOGLE_GENAI_USE_VERTEXAI", None)
            os.environ["GEMINI_MODE"] = mode
            _configure_gemini_cli(mode, key)
            if verbose:
                name = "Vertex / Agent Platform (Path A)" if mode == "vertex" else "Gemini Developer API (Path B)"
                print(f"Connected via the {name} endpoint.")
                if known in ("vertex", "dev") and mode != known:
                    print("Note: your key actually belongs to the other path than you answered — "
                          "no problem, I reconfigured everything for the path that works.")
            return client
        except Exception as e:  # try the other endpoint before giving up
            errors.append(f"[{mode}] {e}")

    raise RuntimeError(_diagnose(errors))


def _diagnose(errors):
    """Turn Google's error salad into one plain instruction."""
    text = "\n".join(errors)
    hints = []
    if "prepayment credits are depleted" in text or "prepay" in text:
        hints.append(
            "YOUR SPECIFIC PROBLEM: your AI Studio project has a prepaid billing plan "
            "with no credits on it — and attaching billing removes the free tier from a "
            "project. THE FIX: open https://aistudio.google.com, use the key/project menu "
            "to create a NEW API key in a NEW project (one with no billing plan), then "
            "delete ~/.course_env and rerun: bash check_setup.sh")
    if "API_KEY_SERVICE_BLOCKED" in text and not hints:
        hints.append(
            "YOUR SPECIFIC PROBLEM: this key is an AI Studio (Path B) key, which cannot "
            "be used on the Vertex platform. THE FIX: rerun 'bash check_setup.sh' and "
            "answer B when asked for your path — or, if you meant to do Path A, create "
            "the key inside the studio page (Block 0, Path A, step 4).")
    if "disallows API keys" in text:
        hints.append(
            "YOUR SPECIFIC PROBLEM: you are on an organization-managed Google account "
            "that blocks API keys. THE FIX: switch to a personal Gmail — see the "
            "'API Keys are Disallowed' box in Block 0, Path A.")
    if "SERVICE_DISABLED" in text and not hints:
        hints.append(
            "YOUR SPECIFIC PROBLEM: the key's project doesn't have the needed service "
            "switched on. THE FIX: create a fresh key from the studio page (Block 0, "
            "Path A step 4) — it comes with the service enabled — then delete "
            "~/.course_env and rerun: bash check_setup.sh")
    if ("API_KEY_INVALID" in text or "API key not valid" in text) and not hints:
        hints.append(
            "YOUR SPECIFIC PROBLEM: the key itself was not accepted — usually a copy-paste "
            "slip (missing characters, extra spaces). THE FIX: delete ~/.course_env, copy "
            "the key again carefully, and rerun: bash check_setup.sh")
    if not hints:
        hints.append(
            "This one isn't in my catalogue — copy this whole message into an email to me "
            "or bring it to a July-10 slot; we'll fix it together in minutes.")
    return ("Could not reach Google with this key.\n\n" + "\n\n".join(hints)
            + "\n\nFull details (for the instructor):\n" + text)
