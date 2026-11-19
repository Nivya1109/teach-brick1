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

## Conclusion

Reading imagined hand movement works within a person (88.9%) but does not transfer to unseen people with these methods (54.4% / 57.6% vs a 70% gate). Brain patterns are personal: a future device must calibrate to its wearer. That calibration problem is the next brick.

## File guide

- `check_env.py` — Prints the Python version and installed library versions.
- `load_data.py` — Loads subject 1's motor-imagery data and prints channels and T1/T2 counts.
- `preprocess.py` — Filters the EEG, creates epochs, and prints epoch counts and shape.
- `classifier.py` — Runs within-subject CSP+LDA 5-fold cross-validation.
- `evaluate.py` — Runs Attempt 1: CSP+LDA leave-one-subject-out evaluation.
- `evaluate_v2.py` — Runs Attempt 2: Riemannian tangent-space leave-one-subject-out evaluation.
- `results.md` — Records both attempts and their honest pass/fail verdicts.

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
```
