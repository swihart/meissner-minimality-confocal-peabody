# Line-by-line audit of the Peabody width normalization

## 1. Width-two surface formula

The normal-sphere decomposition gives

\[
S_2=8\pi+\Psi(e_1)+\Psi(e_2)+\Psi(e_3).
\]

The subscript records that the assembled Peabody has width two.

## 2. Blaschke identity at width two

For a three-dimensional body of constant width `d`,

\[
V=\frac d2 S-\frac\pi3 d^3.
\]

At `d=2`,

\[
V_2=S_2-\frac{8\pi}{3}.
\]

Substituting the surface formula gives

\[
V_2=\frac{16\pi}{3}+\Psi(e_1)+\Psi(e_2)+\Psi(e_3).
\]

Audit gate: the constant is `8*pi-8*pi/3=16*pi/3`.

## 3. Rescaling width two to width one

Scaling all lengths by `1/2` changes width by `1/2` and volume by `(1/2)^3=1/8`. Hence

\[
V_1=\frac18V_2
=\frac{2\pi}{3}+\frac18\sum_{i=1}^3\Psi(e_i).
\]

Audit gate: there is exactly one volume scaling factor, `1/8`; no extra area factor appears after
Blaschke's identity has already produced a volume.

## 4. Meissner baseline

At the all-zero degeneration,

\[
V_M=\frac{2\pi}{3}+\frac{3\Psi(0)}8.
\]

Using

\[
\Psi(0)=-\frac{2\pi}{\sqrt3}\arccos\frac13
\]

gives

\[
\begin{aligned}
V_M
&=\frac{2\pi}{3}
-\frac{3}{8}\frac{2\pi}{\sqrt3}\arccos\frac13\\
&=\pi\left(\frac23-\frac{\sqrt3}{4}\arccos\frac13\right).
\end{aligned}
\]

The identity `3/(4*sqrt(3))=sqrt(3)/4` is the only radical simplification.

## 5. Definition of the one-pair increment

Define

\[
\Phi(e)=\frac{\Psi(e)-\Psi(0)}8.
\]

Then

\[
\begin{aligned}
V_1-V_M
&=\frac18\left(\sum_i\Psi(e_i)-3\Psi(0)\right)\\
&=\sum_i\frac{\Psi(e_i)-\Psi(0)}8\\
&=\Phi(e_1)+\Phi(e_2)+\Phi(e_3).
\end{aligned}
\]

## 6. Exact symbolic gate

`python/independent_one_pair_rederivation.py` checks symbolically that

\[
\frac18\left(\frac{16\pi}{3}+\Psi_1+\Psi_2+\Psi_3\right)
-\left(\frac{2\pi}{3}+\frac{3\Psi_0}{8}\right)
-\sum_{i=1}^3\frac{\Psi_i-\Psi_0}{8}=0.
\]

No decimal approximation is used in this gate.

## 7. Release conclusion

The correct normalized formula is

\[
\boxed{
V_1=V_M+\Phi(e_1)+\Phi(e_2)+\Phi(e_3).
}
\]

A factor `1/4`, `1/2`, or `1/16` at this stage would be a release-blocking normalization error.
