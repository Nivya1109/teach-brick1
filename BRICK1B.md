# Brick 1b — Calibration-Assisted Reading

## The question

Brick 1 showed a reader trained on other people fails on a new person (54.4% / 57.6% vs a 70% gate). Can the same reader pass if it first calibrates on a small slice of the new person's own data — the way every real brain device does a personal setup?

## Protocol

- Test subjects: 1–10 (same as Brick 1).
- For each test subject: training data = all epochs from the other 9 subjects PLUS that subject's run 6 epochs (the calibration slice).
- Test data = that subject's runs 10 and 14 epochs only. Calibration data is never part of the test data.
- Classifier: CSP (n_components=4, reg=None, log=True, norm_trace=False) + LDA — the same as Brick 1 Attempt 1. The ONLY change from the failed exam is the calibration slice.
- Everything else identical: standardize, 8–30 Hz filter, epochs T1/T2, tmin=0.0, tmax=4.0.

## Gate

Mean accuracy across the 10 test subjects of 70% or more = PASS. Below = FAIL. The gate does not move after results are seen.

## Reporting rule

The result goes into results.md as a new "Brick 1b" section, below the Brick 1 sections, which stay unchanged. One attempt as designed — if it fails, it is recorded as FAIL; any new idea becomes a separate future discussion, not a silent retry.

## Claim if it passes

The reader reads a new person after a short personal calibration.
