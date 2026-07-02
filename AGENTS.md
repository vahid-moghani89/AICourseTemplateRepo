# Context for AI agents working in this repository

*(Students: this is the "context file" the Day-3 primer mentions — agents read it automatically before doing anything. In Session 5 you'll study it; later you'll extend it with your own project context. It is also a live example of why markdown matters: this file is instructions, documentation, and course material at once.)*

## What this repository is

The course repository for "Practical AI for Research" (ERIM Summer School 2026), copied by a PhD student as their personal course workspace. Work happens in assignment folders (`a3/`, `a4/`); the rest is course material and should generally not be modified.

## Ground rules for agents

1. **All data in `data/` and `a4/defaults/` is synthetic.** It is safe to read, process, and send to APIs. Documented data quirks are in `data/README.md` — and that documentation is deliberately incomplete.
2. **Never write to `data/` or other course-material folders.** Cleaned or derived data goes into the current assignment folder's `outputs/`.
3. **Plan first, then stop.** When given a specification, restate your plan and wait for approval before executing. The user will gate your work at checkpoints; expect to show intermediate results (exclusion ledgers, sample rows, example classifications) before continuing.
4. **Show your reasoning for any data exclusion or transformation** — this course grades verification, and silent assumptions are the enemy.
5. **Never touch API keys.** The key lives in `~/.course_env`, outside this repo, and must stay there.

## Useful orientation

- Survey data: `data/synthetic_survey/survey.csv` (1,200 rows; see `data/README.md`)
- Classification sample + codebook: `data/sample_200.csv`, `data/codebook_concerns.md`
- Assignment spec templates: `templates/`
- The student's own project context may be in `my_project.md` — read it if present.
