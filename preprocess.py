import mne
from mne.datasets import eegbci


files = eegbci.load_data(1, runs=[6, 10, 14])
raws = [mne.io.read_raw_edf(file, preload=True) for file in files]
for raw in raws:
    eegbci.standardize(raw)
raw = mne.concatenate_raws(raws)

raw.filter(8.0, 30.0, fir_design="firwin")

events, event_id = mne.events_from_annotations(raw)
print(event_id)

epochs = mne.Epochs(
    raw,
    events,
    event_id={"T1": event_id["T1"], "T2": event_id["T2"]},
    tmin=0.0,
    tmax=4.0,
    baseline=None,
    preload=True,
)

left_count = len(epochs["T1"])
right_count = len(epochs["T2"])
print(f"Left epochs: {left_count}")
print(f"Right epochs: {right_count}")
print(f"Total epochs: {len(epochs)}")
print(f"Epoch shape: {epochs.get_data().shape[1]} x {epochs.get_data().shape[2]}")
