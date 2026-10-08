# Fresh-kernel Mathematica release protocol

## Files replayed

The driver extracts the frozen v4 checkpoint and runs, in this order:

1. `00_run_peabody_component_diagnostic_v4.wl`
2. `01_run_peabody_compressed_audit_v4.wl`
3. `02_run_peabody_primitive_probe_v4_1.wl`
4. `03_prepare_peabody_interval_inputs_v4.wl`

Each file is launched by a separate `wolframscript -file` process, giving it a fresh kernel.

## Required gates

- Component diagnostic: `Pass -> true`.
- Compressed audit: `Pass -> true` and `RUN01_PASS.txt` exists.
- Primitive probe: `ExactLowComplexityObstructionPass -> true`.
- Interval-input scout: `NumericalScoutPass -> true`, while `ProofStatus` remains `NOT_CERTIFIED`.

## Recursive guards

After the four runs, two independent guards scan all generated `.wl` outputs:

- `wolfram/check_proof_critical_outputs.wl` parses each output under `HoldComplete`;
- `python/scan_wolfram_outputs.py` performs a separate text and JSON scan.

Both reject:

- `$Aborted`, `$Failed`, `Indeterminate`, infinities, `Failure`, or `Missing`;
- unresolved `NIntegrate`, `Reduce`, `Resolve`, or `FindInstance`;
- unexpanded placeholder symbols ending in `Expr`;
- missing or false summary gates.

The sole allowed unresolved expression is the optional fixed-rho `Integrate` in
`rt_sector_fixed_rho_primitive.wl`. Its presence confirms that the optional probe did not evaluate; it
is not proof authority.

## Invocation

```bash
WOLFRAMSCRIPT_BIN=/full/path/to/wolframscript \
  release_audit/scripts/run_mathematica_release_audit.sh "$PWD"
```

All outputs are written under `release_audit/results/mathematica/`.
