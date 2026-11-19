# Phase 2 — Offline Closed Loop (Replay)

## The idea

Brick 1 read frozen pieces of old recordings. Phase 2 replays a recording as if it is happening live: the signal arrives piece by piece, the reader answers LEFT or RIGHT in the moment, and each answer is written to a feedback log. This is the first closed loop — the shape of "wearing starts teaching" — tested entirely on recorded data. Nothing is live, nobody wears anything.

## The design

- Person: subject 1 only (Brick 1's finding: personal data must be the main training).
- Train: subject 1's runs 6 and 10, standard pipeline (standardize, 8–30 Hz filter, 4-second epochs), CSP (n_components=4, reg=None, log=True, norm_trace=False) + LDA.
- Replay: subject 1's run 14, cut into its epochs in order, fed one at a time as if live. Run 14 is never used in training.
- For each replayed piece, the program prints one feedback line: piece number, its prediction (LEFT or RIGHT), the true label, and CORRECT or WRONG — and appends the same to feedback_log.csv.
- Final summary printed: total pieces, correct count, replay accuracy %.

## Honesty rule

There is no pass gate in this phase — the loop either runs and logs every piece, or it doesn't. The replay accuracy is reported exactly as it falls, next to the Step 5 number (88.9%, same-session cross-validation) with one sentence noting this test is harder because run 14 is a separate session the reader never trained on.

## What this is not

Not live data, not a device, not teaching — it is a reader responding in the moment to a replayed signal.
