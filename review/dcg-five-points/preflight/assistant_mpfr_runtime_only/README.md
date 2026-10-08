# Assistant MPFR preflight — not the final journal replay

These files document an independent C/MPFR preflight executed against the MPFR 4.2.2 runtime library in the assistant container.  The container did not contain the official development header, so the preflight binary used archived ABI declarations.

The results are internally consistent and passed 384-bit, 512-bit, reverse-order, under-resolution, sign-mutation, and overlap audits.  They motivated the current checkpoint, but they are **not promoted as the final DCG proof authority**.  The supplied release build script now requires the official `mpfr.h`; the author's local official-header replay is mandatory before Reviewer Point 2 is closed.
