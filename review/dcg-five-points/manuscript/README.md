# Current DCG review manuscript

The corrected review source is `main_dcg_closeout_review.tex`; it requires
`generated_enclosure_reconciliation_closeout.tex`. The reconciled source/PDF
pair from input commit `ab320cf` is retained unchanged under
`main_dcg_revision_enclosure_reconciled.*`. Earlier checkpoint and Points 1/3
files are historical drafts.

Build the corrected source from this directory:

```bash
bash build_closeout.sh
```

The default uses the author's New TX fonts. For a portable review PDF when New
TX is unavailable, use `bash build_closeout.sh --portable-fonts`; this selects
Latin Modern and can change pagination, but not the formulas. The supplied
closeout preview was built using this documented fallback. `build.sh` now
delegates to the corrected source. A missing reconciliation table is an error.

The scalar proof authority is the archived `python-flint==0.9.0` Arb replay.
Its rational targets remain `Phi(1)>1/4000` and `Phi''<-1/100000`. The historical
official-header MPFR workflow is not an outstanding gate for this Arb route.

This remains a review draft. External geometry/source-convention and formula
proofreading are not documented as completed. Before freezing a submission,
resolve that gate, review the AI-assistance and code-availability statements,
and remove the draft-status author footnote. No submission branch or release
has been created by this closeout audit.
