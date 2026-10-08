(* ::Package:: *)

(*
  Confocal Peabody compressed exponential-rapidity core, v4.

  Important v4 repair:
  Wolfram Language input files evaluate an expression as soon as it is
  syntactically complete.  Therefore a new line beginning with + or - must
  not be used to continue an already complete assignment.  Every multi-term
  definition below uses explicit Plus[...] and Times[...] forms.
*)

ClearAll[
  kappa, rhoFromE, eFromRho,
  rrho, xx, zz,
  d2Expr, dExpr, r2ZExpr, t2ZExpr, r2XExpr, t2XExpr, rExpr, tExpr,
  amExpr, apExpr, deltaExpr, mExpr, cExpr, yExpr, atanArgExpr,
  angleExpr,
  p0Term1Expr, p0Term2Expr, p0DirectExpr, q0Expr, hCompactExpr,
  h0Expr, bcoefExpr, ccoefExpr, prefExpr,
  nfBaseExpr, f0ZExpr, a1Expr, a2Expr, a3Expr, ngBaseExpr, g0ZExpr,
  fNumExpr, gNumExpr, pArcFZExpr, pArcGZExpr,
  p0TExpr, p0RTExpr, p0DecomposedExpr,
  pArcTExpr, pArcRTExpr, pArcExpr,
  angleRhoExpr, qAlgFromQ0Expr, qAlgFromAngleExpr, qAlgExpr,
  dHdLambdaExpr, phiLambdaIntegrandExpr,
  c0Expr, ecoefExpr, fNum0Expr, fNum1Expr,
  u0Expr, u1Expr, uZExpr, jTSectorExpr,
  gNum0Expr, gNum1Expr, gNum2Expr, gNum3Expr,
  a0Expr, b0Expr, v0CandidateExpr, v1CandidateExpr,
  obstructionZ2Expr, obstructionZ1Expr,
  hCompactArcPrimaryExpr, hCompactArcCorrectionExpr,
  hCompactArcExpr, hCompactAlgebraicExpr,
  dHdLambdaDirectExpr, dHdLambdaSectorExpr
];

kappa = 1 + Sqrt[2];

rhoFromE[e_] := kappa*Sqrt[(1 + e)/(1 - e)];
eFromRho[rho_] := (rho^2 - kappa^2)/(rho^2 + kappa^2);

d2Expr = rrho^4 + 1;
dExpr = Sqrt[d2Expr];
r2ZExpr = d2Expr - 2*rrho^2*zz;
t2ZExpr = 2*kappa^2*d2Expr + (rrho^2 - kappa^2)^2*zz;
r2XExpr = r2ZExpr /. zz -> xx^2;
t2XExpr = t2ZExpr /. zz -> xx^2;
rExpr = Sqrt[r2XExpr];
tExpr = Sqrt[t2XExpr];
amExpr = rrho^2 - kappa^2;
apExpr = rrho^2 + kappa^2;

cExpr = amExpr*rExpr/(apExpr*dExpr);
yExpr = (rrho^2 + 1 - dExpr)/(Sqrt[2]*rrho);
atanArgExpr = yExpr*Sqrt[(1 + cExpr)/(1 - cExpr)];
angleExpr = ArcTan[atanArgExpr];

deltaExpr = rExpr - rrho^2 + 1;
mExpr = amExpr*(rrho^2 + 1)*rExpr - apExpr*d2Expr;

p0Term1Expr = Times[
  -16, Sqrt[2], kappa, d2Expr,
  Power[rExpr, -1], Power[tExpr, -1]
];

p0Term2Expr = Times[
  -4, amExpr, apExpr, d2Expr, deltaExpr, mExpr,
  Power[rrho, -4], Power[rExpr, -1], Power[tExpr, -3]
];

p0DirectExpr = Plus[p0Term1Expr, p0Term2Expr];

q0Expr = Times[
  -4, amExpr, apExpr, d2Expr, deltaExpr,
  Power[rrho, -2], Power[rExpr, -1], Power[t2XExpr, -1]
];

hCompactExpr = Plus[Times[p0DirectExpr, angleExpr], q0Expr];

h0Expr = rrho^2 - 1;
bcoefExpr = amExpr*(rrho^2 + 1);
ccoefExpr = apExpr*d2Expr;
prefExpr = -4*amExpr*apExpr*d2Expr/rrho^4;

nfBaseExpr = -prefExpr*(ccoefExpr + h0Expr*bcoefExpr);
f0ZExpr = nfBaseExpr/t2ZExpr^2;

a1Expr = -16*Sqrt[2]*kappa*d2Expr;
a2Expr = prefExpr*bcoefExpr;
a3Expr = prefExpr*h0Expr*ccoefExpr;
ngBaseExpr = Expand[Plus[Times[a1Expr, t2ZExpr], Times[a2Expr, r2ZExpr], a3Expr]];
g0ZExpr = ngBaseExpr/(r2ZExpr*t2ZExpr^2);

p0TExpr = Times[Sqrt[t2XExpr], f0ZExpr /. zz -> xx^2];
p0RTExpr = Times[Sqrt[r2XExpr*t2XExpr], g0ZExpr /. zz -> xx^2];
p0DecomposedExpr = Plus[p0TExpr, p0RTExpr];

fNumExpr = Expand[
  Times[
    rrho,
    Plus[
      Times[D[nfBaseExpr, rrho], t2ZExpr],
      Times[-3/2, nfBaseExpr, D[t2ZExpr, rrho]]
    ]
  ]
];
pArcFZExpr = fNumExpr/t2ZExpr^3;

gNumExpr = Expand[
  Times[
    rrho,
    Plus[
      Times[D[ngBaseExpr, rrho], r2ZExpr, t2ZExpr],
      Times[-1/2, ngBaseExpr, D[r2ZExpr, rrho], t2ZExpr],
      Times[-3/2, ngBaseExpr, D[t2ZExpr, rrho], r2ZExpr]
    ]
  ]
];
pArcGZExpr = gNumExpr/(r2ZExpr^2*t2ZExpr^3);

pArcTExpr = Times[Sqrt[t2XExpr], pArcFZExpr /. zz -> xx^2];
pArcRTExpr = Times[Sqrt[r2XExpr*t2XExpr], pArcGZExpr /. zz -> xx^2];
pArcExpr = Plus[pArcTExpr, pArcRTExpr];

angleRhoExpr = D[angleExpr, rrho];
qAlgFromQ0Expr = rrho*D[q0Expr, rrho];
qAlgFromAngleExpr = rrho*p0DirectExpr*angleRhoExpr;
qAlgExpr = Plus[qAlgFromQ0Expr, qAlgFromAngleExpr];

dHdLambdaExpr = Plus[Times[pArcExpr, angleExpr], qAlgExpr];
phiLambdaIntegrandExpr = dHdLambdaExpr/8;

c0Expr = 2*kappa^2*d2Expr;
ecoefExpr = amExpr^2;
fNum0Expr = Coefficient[fNumExpr, zz, 0];
fNum1Expr = Coefficient[fNumExpr, zz, 1];

u0Expr = Cancel[fNum0Expr/c0Expr];
u1Expr = Cancel[(fNum1Expr + 2*ecoefExpr*u0Expr)/(3*c0Expr)];
uZExpr = (u0Expr + u1Expr*zz)/t2ZExpr^2;
jTSectorExpr = xx*Sqrt[t2XExpr]*(uZExpr /. zz -> xx^2);

gNum0Expr = Coefficient[gNumExpr, zz, 0];
gNum1Expr = Coefficient[gNumExpr, zz, 1];
gNum2Expr = Coefficient[gNumExpr, zz, 2];
gNum3Expr = Coefficient[gNumExpr, zz, 3];

a0Expr = d2Expr;
b0Expr = 2*rrho^2;
v0CandidateExpr = Cancel[gNum0Expr/(a0Expr*c0Expr)];
v1CandidateExpr = Cancel[gNum3Expr/(b0Expr*ecoefExpr)];

obstructionZ2Expr = Cancel[
  Plus[
    gNum2Expr,
    Times[2, b0Expr, c0Expr, v1CandidateExpr],
    Times[-3, b0Expr, ecoefExpr, v0CandidateExpr]
  ]
];

obstructionZ1Expr = Cancel[
  Plus[
    gNum1Expr,
    Times[-3, a0Expr, c0Expr, v1CandidateExpr],
    Times[2, a0Expr, ecoefExpr, v0CandidateExpr]
  ]
];

hCompactArcPrimaryExpr = p0Term1Expr*angleExpr;
hCompactArcCorrectionExpr = p0Term2Expr*angleExpr;
hCompactArcExpr = Plus[hCompactArcPrimaryExpr, hCompactArcCorrectionExpr];
hCompactAlgebraicExpr = q0Expr;
dHdLambdaDirectExpr = rrho*D[hCompactExpr, rrho];
dHdLambdaSectorExpr = dHdLambdaExpr;
