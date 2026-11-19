import mne
import numpy as np
from mne.datasets import eegbci
from pyriemann.estimation import Covariances
from pyriemann.tangentspace import TangentSpace
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


subject_epochs = {}

for subject in range(1, 11):
    files = eegbci.load_data(subject, runs=[6, 10, 14])
    raws = [mne.io.read_raw_edf(file, preload=True) for file in files]
    for raw in raws:
        eegbci.standardize(raw)
    raw = mne.concatenate_raws(raws)
    raw.filter(8.0, 30.0, fir_design="firwin")

    events, event_id = mne.events_from_annotations(raw)
    epochs = mne.Epochs(
        raw,
        events,
        event_id={"T1": event_id["T1"], "T2": event_id["T2"]},
        tmin=0.0,
        tmax=4.0,
        baseline=None,
        preload=True,
    )

    subject_epochs[subject] = (
        epochs.get_data(),
        (epochs.events[:, 2] == event_id["T2"]).astype(int),
    )

accuracies = {}

for held_out_subject in range(1, 11):
    train_X = []
    train_y = []

    for subject, (X, y) in subject_epochs.items():
        if subject != held_out_subject:
            train_X.append(X)
            train_y.append(y)

    test_X, test_y = subject_epochs[held_out_subject]
    train_X = np.concatenate(train_X, axis=0)
    train_y = np.concatenate(train_y, axis=0)

    pipeline = Pipeline(
        [
            ("covariances", Covariances(estimator="oas")),
            ("tangent_space", TangentSpace()),
            ("logistic_regression", LogisticRegression(max_iter=1000)),
        ]
    )
    pipeline.fit(train_X, train_y)
    accuracy = pipeline.score(test_X, test_y)
    accuracies[held_out_subject] = accuracy

    print(f"Subject {held_out_subject}: {accuracy * 100:.1f}%")

mean_accuracy = float(np.mean(list(accuracies.values())))
print(f"Mean LOSO accuracy (Attempt 2): {mean_accuracy * 100:.1f}%")

verdict = "PASS" if mean_accuracy >= 0.70 else "FAIL"

attempt_2 = [
    "",
    "## Attempt 2",
    "",
    "This method estimated OAS covariance matrices for each epoch and mapped them into tangent space.",
    "A logistic regression classifier then learned left-versus-right motor imagery across the nine training subjects.",
    "The held-out subject was tested without appearing in training.",
    "",
    "| Subject | Accuracy |",
    "| --- | ---: |",
]

for subject, accuracy in accuracies.items():
    attempt_2.append(f"| {subject} | {accuracy * 100:.1f}% |")

attempt_2.extend(
    [
        "",
        f"Mean LOSO accuracy (Attempt 2): {mean_accuracy * 100:.1f}%",
        "Fixed gate: 70%",
        f"Verdict: {verdict}",
    ]
)

with open("results.md", "a", encoding="utf-8") as results_file:
    results_file.write("\n" + "\n".join(attempt_2) + "\n")
