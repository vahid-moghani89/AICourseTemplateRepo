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

MODEL = "gemini-2.5-flash"
_ENV_FILE = pathlib.Path.home() / ".course_env"


def _load_env():
    if _ENV_FILE.exists():
        for line in _ENV_FILE.read_text().splitlines():
            if line.startswith("export ") and "=" in line:
                k, v = line[len("export "):].split("=", 1)
                os.environ.setdefault(k, v.strip().strip('"'))


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
    if not key:
        raise RuntimeError("No API key stored yet — run: bash check_setup.sh")

    from google import genai

    known = os.environ.get("GEMINI_MODE")
    candidates = [known] if known in ("vertex", "dev") else ["vertex", "dev"]
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
                name = "Vertex / Agent Platform" if mode == "vertex" else "Gemini Developer API"
                print(f"Connected via the {name} endpoint.")
            return client
        except Exception as e:  # try the other endpoint before giving up
            errors.append(f"[{mode}] {e}")

    raise RuntimeError(
        "Could not reach Google on either endpoint with this key.\n"
        "Most common fixes: (1) re-create the key inside the studio page "
        "(Block 0, Path A step 4) or at aistudio.google.com (Path B), then "
        "delete ~/.course_env and rerun 'bash check_setup.sh'. "
        "(2) If the error below mentions SERVICE_DISABLED, the key's project "
        "doesn't have the service switched on — a fresh key from the studio "
        "page usually comes with it enabled.\n\nDetails:\n" + "\n".join(errors)
    )
