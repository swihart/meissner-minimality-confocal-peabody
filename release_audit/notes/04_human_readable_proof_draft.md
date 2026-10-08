# A human-readable proof of Meissner minimality in the regular-tetrahedron confocal Peabody family

## The theorem

For every width-one regular-tetrahedron confocal Peabody with parameters

\[
(e_1,e_2,e_3)\in[0,1)^3
\]

and any of the eight ways of assigning the two confocal devices to the members of the three
opposite-edge pairs,

\[
V\ge V_M,
\]

where

\[
V_M=\pi\left(\frac23-\frac{\sqrt3}{4}\arccos\frac13\right).
\]

Equality holds exactly when

\[
e_1=e_2=e_3=0.
\]

These equality cases are the two classical Meissner degenerations within the family.

The theorem is only about regular-tetrahedron confocal Peabodies. It is not a proof that the
Meissner bodies minimize volume among all three-dimensional bodies of constant width.

## 1. Why every object under discussion has constant width

Arelio, Montejano, and Oliveros construct a Peabody from three pairs of confocal pea-pod devices.
Each pair replaces the neighborhoods of a pair of opposite tetrahedral edges by two wedge-pod
surfaces. Four spherical caps fill the remaining vertex regions.

Their confocal identity says that if `x` and `y` are centers on the paired confocal strings, then

\[
|x-y|+R(x)+R(y)=2.
\]

The two corresponding boundary points are therefore joined by a length-two binormal. After all six
wedge-pod patches and four caps are assembled, the resulting surface bounds a convex body of width
two. Scaling by one half produces a width-one body.

This source theorem supplies feasibility. The rest of the proof compares volumes inside that explicit
family.

## 2. The normal sphere removes the four caps

Fix a generic Peabody. Let `Omega_A,...,Omega_D` be the Gauss images of the four spherical caps.
Because each cap lies on a sphere of radius two centered at a tetrahedral vertex, a cap point with
outward normal `n` has the opposite support point at the center vertex. Consequently, the normal cone
at that vertex is exactly the antipodal cap image.

For each opposite-edge pair, the two wedge-pod surfaces are paired by length-two binormals, so their
Gauss images are antipodal. If `Gamma_i` denotes one image from pair `i`, the smooth Gauss images and
the four vertex normal cones partition the unit sphere, apart from seams of area zero. Hence

\[
4\pi=2\sum_v|\Omega_v|+2\sum_{i=1}^3|\Gamma_i|.
\]

A radius-two spherical cap has physical area four times the area of its Gauss image. Therefore the
sum of the four cap areas is

\[
8\pi-4\sum_{i=1}^3|\Gamma_i|.
\]

After adding the six wedge-pod areas, the complete width-two surface area is

\[
S_2=8\pi+\sum_{i=1}^3\Psi(e_i),
\]

where

\[
\Psi(e_i)=|W_i^+|+|W_i^-|-4|\Gamma_i|.
\]

This is the key structural step: the three edge-pair parameters no longer interact.

Exchanging the elliptic and hyperbolic devices in a pair only exchanges the two physical wedge
surfaces. Their sum is unchanged, and the antipodal Gauss images have equal area. Thus the eight
orientation patterns all have the same volume for a fixed parameter triple.

## 3. The one-pair formula

For one pair, choose the canonical confocal coordinates

\[
X(t)=a\sin t\,k+b\cos t\,p,
\qquad
Y(\xi)=ae\cosh\xi\,k+b\sinh\xi\,q,
\]

with

\[
b=a\sqrt{1-e^2},
\qquad
b^2=\frac{3+3e^2+4\sqrt2\,e}{1-e^2}.
\]

The center distance and sphere radii are

\[
d=a(\cosh\xi-e\sin t),
\]

\[
R_E=ae(\sin t-u),
\qquad
R_H=a(v-\cosh\xi),
\]

and satisfy

\[
d+R_E+R_H=2.
\]

The unit normal map is conformal in these coordinates:

\[
n_t\cdot n_\xi=0,
\qquad
\|n_t\|=\|n_\xi\|=\frac bd.
\]

Hence

\[
d\omega=\frac{b^2}{d^2}\,dt\,d\xi.
\]

Differentiating the two wedge parametrizations and using the confocal identity gives their area
elements. Combining the two wedge areas with the Gauss-image subtraction yields

\[
\Psi(e)
=-2b^2\int_\theta^{\pi-\theta}\int_{-\eta}^{\eta}
\frac{d+R_ER_H}{d^2}\,d\xi\,dt.
\]

The inner integral is elementary. After carrying it out and then using the beam coordinate
`x=b cos(t)`, one obtains a fixed-domain representation

\[
\Psi(e)=\int_0^1 H(e,x)\,dx.
\]

The frozen theorem package contains the explicit formula for `H`. The release audit implements this
formula independently in Python, Mathematica, and R.

At the Meissner endpoint,

\[
\Psi(0)=-\frac{2\pi}{\sqrt3}\arccos\frac13.
\]

## 4. Width normalization and the scalar increment

Blaschke's identity for a width-`d` body is

\[
V=\frac d2S-\frac\pi3d^3.
\]

At width two,

\[
V_2=S_2-\frac{8\pi}{3}
=\frac{16\pi}{3}+\sum_{i=1}^3\Psi(e_i).
\]

Scaling by one half changes volume by `1/8`, so at width one

\[
V_1=\frac{2\pi}{3}+\frac18\sum_{i=1}^3\Psi(e_i).
\]

At the all-zero Meissner degeneration,

\[
V_M=\frac{2\pi}{3}+\frac{3\Psi(0)}8.
\]

Define

\[
\Phi(e)=\frac{\Psi(e)-\Psi(0)}8.
\]

Then the exact family reduction is

\[
\boxed{
V_1=V_M+\Phi(e_1)+\Phi(e_2)+\Phi(e_3).
}
\]

It remains only to prove that `Phi(e)` is positive for every nonzero admissible parameter.

## 5. Positivity near the Meissner endpoint

Since `Phi(0)=0`, no uniform positive lower bound can hold on a closed interval beginning at zero.
The certificate instead studies

\[
J(e)=\frac{\Phi(e)}e,
\]

with the continuous extension

\[
J(0)=\Phi'(0).
\]

The exact endpoint derivative is

\[
\Phi'(0)=\frac12\left[
\frac{5\pi}{3\sqrt3}-3
+\arccos\!\frac13
\left(\frac{3\sqrt2}{2}-\frac{5\sqrt6\pi}{18}\right)
\right]>0.
\]

An outward-rounded interval calculation proves

\[
\Phi'(e)>\frac1{2000}
\qquad
\left(0\le e\le\frac1{100}\right).
\]

Therefore

\[
\Phi(e)=\int_0^e\Phi'(t)\,dt\ge\frac e{2000},
\]

so

\[
\frac{\Phi(e)}e\ge\frac1{2000}
\qquad
\left(0<e\le\frac1{100}\right).
\]

The continuous endpoint value is included through the exact formula for `Phi'(0)`.

## 6. Positivity on the compact central interval

On

\[
\frac1{100}\le e\le\frac{199}{200},
\]

the proof certifies `Phi` directly. It uses the stable parameter

\[
q=\frac{1-e}{1+e}
\]

and the fixed integral

\[
\Psi(q)=\int_0^1H(q,x)\,dx.
\]

For each rational parameter slab, the `x` integral is enclosed by a composite midpoint rule with an
outward interval second-derivative remainder. A centered mean-value form in `q` then encloses the
integral simultaneously for every parameter in the slab.

The final exact partition contains 43 parameter slabs and ten `x` panels per slab. Every slab proves

\[
\Phi(e)>\frac1{10^7}.
\]

The weakest raw lower bound is

\[
3.2899516603979685\times10^{-7}.
\]

## 7. Positivity on the tail

The remaining interval

\[
\frac{199}{200}\le e<1
\]

is represented by

\[
0<q\le\frac1{399}.
\]

The stable `q` formula extends continuously to `q=0`. A direct outward-rounded interval Riemann
certificate on 2,000 rational rectangles proves

\[
\Phi(e)>\frac1{20000}
\qquad
\left(\frac{199}{200}\le e<1\right).
\]

The central and tail certificates meet exactly because

\[
\frac{1-199/200}{1+199/200}=\frac1{399}.
\]

There is no open seam or floating-point endpoint conversion.

## 8. Completion and equality

The three certificate blocks prove

\[
\Phi(e)>0\qquad(0<e<1),
\]

while `Phi(0)=0`. Therefore each summand in

\[
V_1-V_M=\Phi(e_1)+\Phi(e_2)+\Phi(e_3)
\]

is nonnegative. Hence `V_1>=V_M`.

If equality holds, a sum of three nonnegative quantities is zero, so all three quantities vanish.
Since `Phi(e)=0` only at `e=0`,

\[
e_1=e_2=e_3=0.
\]

Conversely, the all-zero parameter triple is the Meissner degeneration and has volume `V_M`.
This proves the theorem.

## 9. Computer-assisted trust boundary

The source geometry and the additive formula are exact mathematical derivations. The scalar positivity
statement is computer-assisted:

- rational parameter partitions and endpoint identities are exact;
- `mpmath.iv` supplies outward-rounded interval arithmetic;
- central and tail certificates have independent precision and adversarial replays;
- the release audit supplies a second Python checker with a different derivative implementation;
- Mathematica and R are independent semantic checks, not the principal proof authority.

The theorem has exactly the restricted-family scope stated at the beginning.
