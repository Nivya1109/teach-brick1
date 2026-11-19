import mne
from mne.datasets import eegbci


files = eegbci.load_data(1, runs=[6, 10, 14])
raws = [mne.io.read_raw_edf(file, preload=True) for file in files]
raw = mne.concatenate_raws(raws)

print(raw.ch_names)

events, event_id = mne.events_from_annotations(raw)
left_count = sum(event_id["T1"] == event for event in events[:, 2])
right_count = sum(event_id["T2"] == event for event in events[:, 2])

print(f"Left imagined (T1): {left_count}")
print(f"Right imagined (T2): {right_count}")
