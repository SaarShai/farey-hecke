# UCI human-workflow pilot manifests

Status: **ready for a real participant; no human result is claimed**.

These are three matched, label-blind browser manifests for the frozen UCI
Optical Recognition of Handwritten Digits workload. Every condition contains
the same 100 items (10 per model-predicted digit, selected round-robin across
the frozen margin bins) and differs only in item order:

- `manifest-production.json`
- `manifest-seeded_random.json`
- `manifest-quota_balanced.json`

The prompts contain only 8x8 feature renderings and the ten digit choices. The
test-label column was not read or written by the exporter. The labels remain
reserved for a later reveal/analysis step.

## Frozen provenance

- UCI archive SHA-256: `0d7b054fea010270e9b3f06411c654c5e59547732ad626381980baffe0a23fb0`
- UCI label-blind freeze SHA-256: `43af5bdcc36bc1d53fbdd6aca5781ad65e00ddcbf39c222d9eed1679cc25c7f8`
- Common cohort digest: `932edfc21d60a41873e0bd5ef0b3a65bf581a82016b788bc5c8c05d0a4c98812`

| condition | manifest SHA-256 | order digest |
|---|---|---|
| production | `84b22ab4c45644942debac1c35440346bada71bc39db8f2d4abf11b66e25feb2` | `6bf5b9e46ad46d38b2882e958f087692b4b6c8d2c441ffd8e952a81b96e34c9e` |
| seeded random | `a33d448fec40ca4ad5d2b640def4945b985bec51d663bdcf6fddb3b30a99a99b` | `5f20136284bb3cc45cd6a7e16423de5f43a0362860e0a272dc4233f20bf86a50` |
| quota balanced | `ccf83b2efa16a47abc219c03621569a1dc0610a89af43d75020165f7ab79549d` | `24407af3adbaef9f80704911866e96279730765fd2e1e994df7e4cea66766687` |

## Run protocol

1. Start the loopback server from the project root and open `/pilot.html`.
2. Assign one manifest per session in counterbalanced order; do not let the
   participant see the other conditions or any ground-truth labels.
3. Use a pseudonymous session ID and the approved loaded reviewer rate.
4. Download the JSONL evidence after each sealed session and verify it with:

   ```bash
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
     python3 workflow_measurement.py session.jsonl --json
   ```

5. Only after all sessions are sealed, reveal the UCI labels and calculate
   accuracy/error by condition. A positive result requires lower active time or
   total cost without a material error, skip, correction, or adjudication
   increase. A neutral or negative result remains valid evidence.

The 100-item workload is a feasibility pilot, not a powered claim about all
human digit recognition. Any customer or professional study should use the
same frozen-order protocol on its real workload.
