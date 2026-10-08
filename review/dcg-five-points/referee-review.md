# Five-point major-revision review

## What must be proved or supplied before acceptance

1. **Convexity and constant width across the entire parameter range.**  Make precise, for every parameter and orientation, the application of the source Peabody construction and prove the almost-everywhere Gauss-sphere partition used by the area bookkeeping.
2. **Interval-arithmetic trust boundary.**  Replace or independently confirm the `mpmath.iv` proof authority with a more heavily vetted rigorous arithmetic implementation, with particular attention to directed rounding for `sqrt` and `atan` and to the certificate's numerical headroom.
3. **Formula derivations and global branch control.**  Supply the steps behind the one-pair formula, fixed-interval reduction, stable chart, and principal `arctan` branch.
4. **Smooth extension to the parabolic endpoint.**  Prove that the stable chart and the derivatives used in the concavity certificate have genuine removable singularities and extend regularly to the endpoint.
5. **Equality classes and seams.**  Explain why the eight zero-parameter orientation patterns form exactly the two classical Meissner congruence classes, and justify the measure-zero seam statement used in the normal-area calculation.

The review recommends major revision and views Points 1--3 as mandatory acceptance gates.
