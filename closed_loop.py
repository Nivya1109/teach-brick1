import csv

import mne
import numpy as np
from mne.datasets import eegbci
from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.pipeline import Pipeline


def get_epochs(runs):
    files = eegbci.load_data(1, runs=list(runs))
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


train_X_parts = []
train_y_parts = []
for runs in ([6], [10]):
    X, y = get_epochs(runs)
    train_X_parts.append(X)
    train_y_parts.append(y)

train_X = np.concatenate(train_X_parts, axis=0)
train_y = np.concatenate(train_y_parts, axis=0)

pipeline = Pipeline(
    [
        ("csp", CSP(n_components=4, reg=None, log=True, norm_trace=False)),
        ("lda", LinearDiscriminantAnalysis()),
    ]
)
pipeline.fit(train_X, train_y)

replay_X, replay_y = get_epochs([14])
correct_count = 0

with open("feedback_log.csv", "w", newline="", encoding="utf-8") as log_file:
    writer = csv.writer(log_file)
    writer.writerow(["piece", "prediction", "true_label", "result"])

    for piece_number, (epoch, true_label) in enumerate(
        zip(replay_X, replay_y), start=1
    ):
        predicted_label = int(pipeline.predict(epoch[np.newaxis, ...])[0])
        prediction = "RIGHT" if predicted_label == 1 else "LEFT"
        true_name = "RIGHT" if int(true_label) == 1 else "LEFT"
        result = "CORRECT" if predicted_label == int(true_label) else "WRONG"

        if result == "CORRECT":
            correct_count += 1

        print(
            f"Piece {piece_number}: predicted {prediction} "
            f"| true {true_name} | {result}"
        )
        writer.writerow([piece_number, prediction, true_name, result])

total_pieces = len(replay_y)
replay_accuracy = correct_count / total_pieces * 100
print(
    f"Replay total: {total_pieces} | Correct: {correct_count} "
    f"| Replay accuracy: {replay_accuracy:.1f}%"
)

phase2_section = [
    "",
    "## Phase 2 — Offline Closed Loop",
    "",
    "The Phase 2 reader trained on subject 1 runs 6 and 10, then replayed run 14 one epoch at a time as if live.",
    "Run 14 was never used for training, and every replayed piece was printed and written to feedback_log.csv.",
    f"Replay accuracy: {replay_accuracy:.1f}% ({correct_count}/{total_pieces} correct)",
    "Step 5 scored 88.9% with same-session cross-validation; this replay test is harder because run 14 is a separate session the reader never trained on.",
]

with open("results.md", "a", encoding="utf-8") as results_file:
    results_file.write("\n".join(phase2_section) + "\n")
