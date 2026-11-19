# teach-brick1

## Goal

Brick 1 of Teach. Teach is a wearable gadget idea — wear it, and the brain learns a skill without studying. This repo does NOT build that. This repo only learns to READ one brain pattern from public data. Reading is the first brick.

## Target pattern

Motor imagery — a person imagining moving their left hand vs their right hand.

## Dataset

PhysioNet EEG Motor Movement/Imagery, loaded with the Python library MNE (its eegbci module).

## Pass gate

Left-vs-right classification accuracy of 70% or more on subjects the model was never trained on (leave-one-subject-out). Chance is 50%.

## What this is not

- Not a device that teaches skills — yet.
- No brain stimulation of any kind.
- No medical claims.
- Read-only research on public data.
