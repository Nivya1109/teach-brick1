import mne
import numpy as np
from mne.datasets import eegbci
from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.pipeline import Pipeline


def get_epochs(subject, runs):
    files = eegbci.load_data(subject, runs=list(runs))
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

    X = epochs.get_data()
    y = (epochs.events[:, 2] == event_id["T2"]).astype(int)
    return X, y


full_epochs = {
    subject: get_epochs(subject, [6, 10, 14])
    for subject in range(1, 11)
}
calibration_epochs = {
    subject: get_epochs(subject, [6])
    for subject in range(1, 11)
}
test_epochs = {
    subject: get_epochs(subject, [10, 14])
    for subject in range(1, 11)
}

accuracies = {}

for test_subject in range(1, 11):
    train_X = []
    train_y = []

    for subject, (X, y) in full_epochs.items():
        if subject != test_subject:
            train_X.append(X)
            train_y.append(y)

    calibration_X, calibration_y = calibration_epochs[test_subject]
    train_X.append(calibration_X)
    train_y.append(calibration_y)

    test_X, test_y = test_epochs[test_subject]
    train_X = np.concatenate(train_X, axis=0)
    train_y = np.concatenate(train_y, axis=0)

    pipeline = Pipeline(
        [
            ("csp", CSP(n_components=4, reg=None, log=True, norm_trace=False)),
            ("lda", LinearDiscriminantAnalysis()),
        ]
    )
    pipeline.fit(train_X, train_y)
    accuracy = pipeline.score(test_X, test_y)
    accuracies[test_subject] = accuracy

    print(f"Subject {test_subject}: {accuracy * 100:.1f}%")

mean_accuracy = float(np.mean(list(accuracies.values())))
print(f"Mean Brick 1b accuracy: {mean_accuracy * 100:.1f}%")

verdict = "PASS" if mean_accuracy >= 0.70 else "FAIL"

brick1b_section = [
    "",
    "## Brick 1b — Calibration-Assisted Reading",
    "",
    "For each test subject, CSP+LDA was trained on all epochs from the other nine subjects plus run 6 from the test subject.",
    "Runs 10 and 14 from that test subject were used only for testing, and calibration run 6 was never included in test data.",
    "The method used the same channel standardization, 8–30 Hz filtering, 4-second epochs, CSP settings, and LDA as Brick 1.",
    "",
    "| Subject | Accuracy |",
    "| --- | ---: |",
]

for subject, accuracy in accuracies.items():
    brick1b_section.append(f"| {subject} | {accuracy * 100:.1f}% |")

brick1b_section.extend(
    [
        "",
        f"Mean Brick 1b accuracy: {mean_accuracy * 100:.1f}%",
        "Fixed gate: 70%",
        f"Verdict: {verdict}",
    ]
)

if verdict == "PASS":
    brick1b_section.extend(
        [
            "",
            "The reader reads a new person after a short personal calibration.",
        ]
    )

with open("results.md", "a", encoding="utf-8") as results_file:
    results_file.write("\n".join(brick1b_section) + "\n")
