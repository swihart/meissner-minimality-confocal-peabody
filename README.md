# Confocal Peabody restricted-family minimality certificate

## Principal result

```text
GO_PEABODY_FAMILY_MINIMALITY_CERTIFIED
```

The package certifies that the Meissner volume is minimal among width-one regular-tetrahedron confocal Peabodies, with equality exactly at the all-zero Meissner degeneration.

It does **not** solve the global three-dimensional Blaschke-Lebesgue problem.

## Proof dependencies

1. `certificates/peabody_central_certificate.json` — local endpoint and compact central interval;
2. frozen `confocal_peabody_tail_first_gate_2026-09-30.zip` — certified tail;
3. `data/additivity_audit.json` — normalization, orientation, permutation, and mixed-difference audit;
4. `certificates/peabody_family_certificate.json` — final theorem assembly.

## Replays

From the package root, extract the two frozen dependency ZIPs into temporary directories, then run the commands recorded in `transcripts/`. The central proof authority is:

```bash
python3 python/peabody_central_interval_certificate.py \
  --output-dir certificates/replay_central_80dps \
  --precision-dps 80 \
  --order bfs
```

Expected classification:

```text
GO_PEABODY_CENTRAL_PHI_POSITIVITY_CERTIFIED
```

The complete package validator is:

```bash
python3 python/validate_peabody_family_package.py
```

## Main notes

- `notes/peabody_central_certificate_note.md`
- `notes/peabody_family_minimality_theorem.md`
