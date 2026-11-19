# Teach-Brick1 Project Overview

## The big idea (Teach)

Teach is a long-term idea for a wearable gadget: wear it, and the brain learns a skill without studying. There would be no screen and no lessons. That is the long-term dream this project serves.

## What THIS repo is (Brick 1)

This repository is only the first brick: learning to READ one brain pattern from public data. It does not teach skills, and it claims nothing more.

## Target pattern and data

The target pattern is motor imagery: imagining moving the left hand versus imagining moving the right hand. The data is the PhysioNet EEG Motor Movement/Imagery dataset, loaded in Python with the MNE library.

## Pass gate

The pass gate is fixed in advance: left-versus-right classification accuracy must be 70% or more on subjects the model was never trained on, using leave-one-subject-out evaluation across subjects 1–10. Chance is 50%.

## Full step list

- **Step 0 — Setup (Python, VS Code, Git): DONE** — The Python environment and local Git repository are set up.
- **Step 1 — Charter README + first commit: DONE** — README.md records the project charter and pass gate, and the charter commit is in the Git log.
- **Step 2 — Environment: venv + libraries + check_env.py: DONE** — The `.venv` environment, requirements, environment check script, and ignore rules exist.
- **Step 3 — load_data.py: DONE** — The script loads subject 1's runs 6, 10, and 14 and prints channel names and T1/T2 counts.
- **Step 4 — preprocess.py: DONE** — The script standardizes channels, applies an 8–30 Hz bandpass filter, creates epochs, and prints class counts.
- **Step 5 — classifier.py: NOT STARTED** — It will use CSP and LDA for within-subject cross-validation and must be clearly above 50%.
- **Step 6 — evaluate.py: NOT STARTED** — It will perform leave-one-subject-out evaluation across subjects 1–10 and write honest results to `results.md` for comparison against the 70% gate.
- **Step 7 — Final README write-up: NOT STARTED** — It will complete the final README write-up with a "What this is not" section; GitHub push is allowed only after explicit instruction.

## Files so far

- `README.md` — Describes the project charter, target pattern, dataset, pass gate, and exclusions.
- `requirements.txt` — Lists the four Python libraries needed by the project.
- `check_env.py` — Prints the Python version and the installed library versions.
- `.gitignore` — Excludes the virtual environment, Python cache files, and downloaded data.
- `load_data.py` — Downloads and loads subject 1's motor-imagery runs and prints channels and T1/T2 counts.
- `preprocess.py` — Standardizes channels, filters at 8–30 Hz, creates epochs, and prints epoch counts and shape.
- `PROJECT_OVERVIEW.md` — Documents the whole project, current status, files, rules, and future phases.

## Files planned

- `classifier.py` — Will train CSP plus LDA and report clearly above-chance cross-validation within subject 1.
- `evaluate.py` — Will run leave-one-subject-out evaluation across subjects 1–10.
- `results.md` — Will record each subject result, the overall result, and an honest pass-or-fail comparison with the 70% gate.

## Project rules

- Every git commit must be authored only by me, under my own git name and email.
- Commit messages, code comments, and file contents must contain no AI or Claude mentions and no Co-authored-by lines.
- Never push anything to GitHub without explicit instruction.
- Run every Python script as `.venv/bin/python <filename>`.
- Install Python packages only as `.venv/bin/python -m pip ...`.
- Build and verify one step at a time.
- Report all results honestly, whether they pass or fail.

## What comes after Brick 1

After Brick 1, future work may proceed to an offline closed-loop system (Phase 2), then a live read-only test with a real headband (Phase 3), only after budget allows.
