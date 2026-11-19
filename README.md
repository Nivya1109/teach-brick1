# teach-brick1

## Goal

Brick 1 of Teach. Teach is a wearable gadget idea — wear it, and the brain learns a skill without studying. This repo does NOT build that. This repo only learns to READ one brain pattern from public data. Reading is the first brick.

## What this is not

- Not a device that teaches skills — yet.
- No brain stimulation of any kind.
- No medical claims.
- Read-only research on public data.

## Method

The target pattern is motor imagery: a person imagining moving their left hand versus their right hand.

The data is the PhysioNet EEG Motor Movement/Imagery dataset. This project uses subjects 1–10 and the motor-imagery runs 6, 10, and 14, loaded through MNE's `eegbci` module.

The common pipeline standardizes channel names, applies an 8–30 Hz bandpass filter, and cuts 4-second epochs. T1 represents imagined left-fist movement and T2 represents imagined right-fist movement.

Two classifiers were tried:

- CSP with 4 components plus linear discriminant analysis (CSP+LDA).
- Riemannian covariance estimation with OAS, tangent-space mapping, and logistic regression.

## Results

- Within-subject (subject 1, 5-fold cross-validation): 88.9% accuracy (chance 50%)
- Cross-subject, Attempt 1 (CSP+LDA, leave-one-subject-out): 54.4% — FAIL vs the fixed 70% gate
- Cross-subject, Attempt 2 (Riemannian, leave-one-subject-out): 57.6% — FAIL vs the fixed 70% gate
- Brick 1b (calibration-assisted: train on 9 subjects plus the test subject's run 6, test on runs 10–14, CSP+LDA): 55.3% — FAIL vs the fixed 70% gate

## Conclusion

Reading imagined hand movement works when the model trains mainly on the person's own data (88.9% within-subject). It fails when trained on other people (54.4% / 57.6%), and a small calibration slice mixed into stranger data does not rescue it (55.3%) — the personal data is drowned out. Brain patterns are personal: personal data must be the main ingredient, not a sprinkle. A future device must be trained primarily on its own wearer. The reading chapter is closed with this finding; the next phase is the offline closed loop.

## File guide

- `check_env.py` — Prints the Python version and installed library versions.
- `load_data.py` — Loads subject 1's motor-imagery data and prints channels and T1/T2 counts.
- `preprocess.py` — Filters the EEG, creates epochs, and prints epoch counts and shape.
- `classifier.py` — Runs within-subject CSP+LDA 5-fold cross-validation.
- `evaluate.py` — Runs Attempt 1: CSP+LDA leave-one-subject-out evaluation.
- `evaluate_v2.py` — Runs Attempt 2: Riemannian tangent-space leave-one-subject-out evaluation.
- `evaluate_calibration.py` — Runs the Brick 1b calibration-assisted CSP+LDA evaluation.
- `results.md` — Records both attempts and their honest pass/fail verdicts.
- `BRICK1B.md` — Defines the fixed Brick 1b calibration protocol, gate, and reporting rule.

## How to run

Install the dependencies:

```text
.venv/bin/python -m pip install -r requirements.txt
```

Run the scripts in this order:

```text
.venv/bin/python check_env.py
.venv/bin/python load_data.py
.venv/bin/python preprocess.py
.venv/bin/python classifier.py
.venv/bin/python evaluate.py
.venv/bin/python evaluate_v2.py
.venv/bin/python evaluate_calibration.py
```
