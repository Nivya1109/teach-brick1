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


## Attempt 2

This method estimated OAS covariance matrices for each epoch and mapped them into tangent space.
A logistic regression classifier then learned left-versus-right motor imagery across the nine training subjects.
The held-out subject was tested without appearing in training.

| Subject | Accuracy |
| --- | ---: |
| 1 | 64.4% |
| 2 | 71.1% |
| 3 | 46.7% |
| 4 | 55.6% |
| 5 | 53.3% |
| 6 | 48.9% |
| 7 | 60.0% |
| 8 | 55.6% |
| 9 | 53.3% |
| 10 | 66.7% |

Mean LOSO accuracy (Attempt 2): 57.6%
Fixed gate: 70%
Verdict: FAIL
