# Leave-One-Subject-Out Results

Each subject was processed with channel standardization, an 8–30 Hz bandpass filter, and 4-second epochs.
CSP extracted four spatial features and LDA classified left versus right motor imagery.
For each result, the model was trained on the other nine subjects and tested only on the held-out subject.
No subject appeared in both the training set and test set for a given result.

| Subject | Accuracy |
| --- | ---: |
| 1 | 48.9% |
| 2 | 68.9% |
| 3 | 48.9% |
| 4 | 46.7% |
| 5 | 53.3% |
| 6 | 40.0% |
| 7 | 51.1% |
| 8 | 68.9% |
| 9 | 48.9% |
| 10 | 68.9% |

Mean LOSO accuracy: 54.4%
Fixed gate: 70%
Verdict: FAIL
