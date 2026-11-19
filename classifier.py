import mne
from mne.datasets import eegbci
from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline


files = eegbci.load_data(1, runs=[6, 10, 14])
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
y = epochs.events[:, 2]
left_id = event_id["T1"]
y = (y == event_id["T2"]).astype(int)

pipeline = Pipeline(
    [
        ("csp", CSP(n_components=4, reg=None, log=True, norm_trace=False)),
        ("lda", LinearDiscriminantAnalysis()),
    ]
)

cross_validation = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
fold_accuracies = cross_val_score(
    pipeline,
    X,
    y,
    cv=cross_validation,
    scoring="accuracy",
)

print(f"Fold accuracies: {[round(score, 4) for score in fold_accuracies].__str__()}")
print(f"Mean accuracy: {fold_accuracies.mean() * 100:.1f}%")
print("Chance level: 50%")
