(* ::Package:: *)

(*
  Confocal Peabody exact-additivity / monotonicity audit
  Date: 2026-09-29

  Purpose
  -------
  The exact regular-tetrahedron Peabody volume has been reduced to

      V_1(e1,e2,e3) = V_M + Phi(e1) + Phi(e2) + Phi(e3),
      Phi(e) = (Psi(e)-Psi(0))/8.

  This Wolfram Language file does four things:

    1. encodes the exact one-dimensional integral for Psi(e);
    2. converts it to two fixed-interval formulations, so differentiation
       under the integral sign has no moving endpoint;
    3. checks the known exact endpoint derivative Phi'(0)>0 and performs
       a high-precision numerical derivative scan;
    4. optionally asks Mathematica for heavier symbolic simplifications,
       a direct rapidity derivative integral, and an integration-by-parts
       decomposition.

  The default run is deliberately moderate.  After it succeeds, set

      RunHeavySymbolics = True;

  below and evaluate the file again.  Heavy steps are protected by
  TimeConstrained and may return $Aborted rather than hanging indefinitely.

  No external Mathematica packages are required.
*)

ClearAll["Global`*"];
$HistoryLength = 0;
$MaxExtraPrecision = 20000;

(* ----------------------------- configuration ----------------------------- *)

RunNumericalAudit = True;
RunEndpointSymbolics = True;
RunHeavySymbolics = False;

WorkingPrecisionGoal = 80;
EndpointTimeLimitSeconds = 300;
HeavyTimeLimitSeconds = 1200;

baseDirectory = If[
  StringQ[$InputFileName] && StringLength[$InputFileName] > 0,
  DirectoryName[$InputFileName],
  Directory[]
];

outputDirectory = FileNameJoin[{baseDirectory, "mathematica_output"}];
If[! DirectoryQ[outputDirectory],
  CreateDirectory[outputDirectory, CreateIntermediateDirectories -> True]
];

reportPath = FileNameJoin[{outputDirectory, "mathematica_run_report.txt"}];
reportStream = OpenWrite[reportPath, PageWidth -> Infinity];

ClearAll[log];
log[msg_String] := (
  Print[msg];
  WriteString[reportStream, msg, "\n"];
  Flush[reportStream]
);
log[msg_] := Module[{s = ToString[msg, InputForm]},
  Print[msg];
  WriteString[reportStream, s, "\n"];
  Flush[reportStream]
];

log["CONFOCAL PEABODY MATHEMATICA AUDIT: START"];
log["Mathematica version: " <> ToString[$Version]];
log["Output directory: " <> outputDirectory];
log["RunHeavySymbolics: " <> ToString[RunHeavySymbolics]];

(* ------------------------------ exact constants -------------------------- *)

alpha = ArcCos[1/3];
meissnerWidth1Exact = Pi (2/3 - Sqrt[3] alpha/4);
psi0Exact = -(2 Pi/Sqrt[3]) alpha;
phiPrime0Exact = 1/2 (
  5 Pi/(3 Sqrt[3]) - 3 +
  alpha (3 Sqrt[2]/2 - 5 Sqrt[6] Pi/18)
);

(* -------------------------- confocal scalar data ------------------------- *)

ClearAll[b2, b, a, theta, eta, u, v, y];

b2[z_] := (3 + 3 z^2 + 4 Sqrt[2] z)/(1 - z^2);
b[z_] := Sqrt[b2[z]];
a[z_] := b[z]/Sqrt[1 - z^2];
theta[z_] := ArcCos[1/b[z]];
eta[z_] := ArcSinh[1/b[z]];

(* Algebraically simpler exact versions of Sin[theta], Cosh[eta], Tanh[eta/2]. *)
u[z_] := Sqrt[1 - 1/b2[z]];
v[z_] := Sqrt[1 + 1/b2[z]];
y[z_] := 1/(Sqrt[b2[z] + 1] + b[z]);

(* -------------------------- original t-integral -------------------------- *)

ClearAll[cT, angleT, kernelIT, coreT];

cT[z_, tt_] := z Sin[tt];
angleT[z_, tt_] := ArcTan[
  y[z] Sqrt[(1 + cT[z, tt])/(1 - cT[z, tt])]
];
kernelIT[z_, tt_] := 4 angleT[z, tt]/Sqrt[1 - cT[z, tt]^2];

coreT[z_, tt_] :=
  kernelIT[z, tt]/a[z] +
  z (Sin[tt] - u[z])/(1 - z^2 Sin[tt]^2) (
    (v[z] z Sin[tt] - 1) kernelIT[z, tt] + 2/b[z]
  );

psiFormalT[z_] := -4 b2[z] Inactive[Integrate][
  coreT[z, t], {t, theta[z], Pi/2}
];

(* ------------------- fixed interval I: beam-coordinate x ----------------- *)

(*
  Set x = b(e) Cos[t].  On the half-domain t in [theta(e),Pi/2],
  x runs from 1 down to 0 and

      Sin[t] = Sqrt[1-x^2/b(e)^2].

  This removes the moving integration endpoint exactly.
*)

ClearAll[amp, cX, angleX, kernelIX, coreX, hFixed];

amp[z_, xx_] := Sqrt[1 - xx^2/b2[z]];
cX[z_, xx_] := z amp[z, xx];
angleX[z_, xx_] := ArcTan[
  y[z] Sqrt[(1 + cX[z, xx])/(1 - cX[z, xx])]
];
kernelIX[z_, xx_] := 4 angleX[z, xx]/Sqrt[1 - cX[z, xx]^2];

coreX[z_, xx_] :=
  kernelIX[z, xx]/a[z] +
  z (amp[z, xx] - u[z])/(1 - cX[z, xx]^2) (
    (v[z] cX[z, xx] - 1) kernelIX[z, xx] + 2/b[z]
  );

hFixed[z_, xx_] := -4 b[z] coreX[z, xx]/amp[z, xx];

psiFormalFixed[z_] := Inactive[Integrate][hFixed[z, x], {x, 0, 1}];

(* ---------------- fixed interval II: tangent-half-angle coordinate ------- *)

(*
  A second exact fixed-domain representation uses q = Tan[t/2].
  The lower endpoint is q0(e)=Tan[theta(e)/2].  Mapping q linearly to
  x in [0,1] gives an independent symbolic form that Mathematica may
  simplify differently.
*)

ClearAll[q0, qMap, hHalfAngle];
q0[z_] := Sqrt[(b[z] - 1)/(b[z] + 1)];
qMap[z_, xx_] := q0[z] + (1 - q0[z]) xx;
hHalfAngle[z_, xx_] :=
  -8 b2[z] (1 - q0[z]) coreT[z, 2 ArcTan[qMap[z, xx]]] /
    (1 + qMap[z, xx]^2);

psiFormalHalfAngle[z_] := Inactive[Integrate][hHalfAngle[z, x], {x, 0, 1}];

(* ---------------- exact formal derivatives under fixed integrals -------- *)

hFixedExpr = hFixed[e, x];
dHdeExpr = D[hFixedExpr, e];
hHalfAngleExpr = hHalfAngle[e, x];
dHHalfAngleDeExpr = D[hHalfAngleExpr, e];

psiPrimeFormal[e_] := Inactive[Integrate][dHdeExpr, {x, 0, 1}];
phiPrimeFormal[e_] := psiPrimeFormal[e]/8;

Put[hFixedExpr,
  FileNameJoin[{outputDirectory, "fixed_interval_integrand.wl"}]
];
Put[dHdeExpr,
  FileNameJoin[{outputDirectory, "fixed_interval_derivative_raw.wl"}]
];
Put[hHalfAngleExpr,
  FileNameJoin[{outputDirectory, "half_angle_integrand.wl"}]
];
Put[dHHalfAngleDeExpr,
  FileNameJoin[{outputDirectory, "half_angle_derivative_raw.wl"}]
];

log["Exact fixed-interval integrands and raw derivatives exported."];

(* --------------------------- numerical evaluators ----------------------- *)

ClearAll[psiN, psiTN, psiHalfAngleN, phiN, phiPrimeN];

psiN[ee_?NumericQ, wp_:WorkingPrecisionGoal] := Module[
  {ep = N[ee, wp], expr},
  If[! TrueQ[0 <= ep < 1], Return[$Failed]];
  expr = hFixedExpr /. e -> ep;
  NIntegrate[
    Evaluate[N[expr, wp]], {x, 0, 1},
    WorkingPrecision -> wp,
    AccuracyGoal -> Floor[0.38 wp],
    PrecisionGoal -> Floor[0.38 wp],
    MinRecursion -> 2,
    MaxRecursion -> 30,
    Method -> {"GlobalAdaptive", "SymbolicProcessing" -> 0}
  ]
];

psiTN[ee_?NumericQ, wp_:WorkingPrecisionGoal] := Module[
  {ep = N[ee, wp], expr, lower},
  If[! TrueQ[0 <= ep < 1], Return[$Failed]];
  expr = -4 b2[ep] coreT[ep, t];
  lower = theta[ep];
  NIntegrate[
    Evaluate[N[expr, wp]], {t, lower, Pi/2},
    WorkingPrecision -> wp,
    AccuracyGoal -> Floor[0.38 wp],
    PrecisionGoal -> Floor[0.38 wp],
    MinRecursion -> 2,
    MaxRecursion -> 30,
    Method -> {"GlobalAdaptive", "SymbolicProcessing" -> 0}
  ]
];

psiHalfAngleN[ee_?NumericQ, wp_:WorkingPrecisionGoal] := Module[
  {ep = N[ee, wp], expr},
  If[! TrueQ[0 <= ep < 1], Return[$Failed]];
  expr = hHalfAngleExpr /. e -> ep;
  NIntegrate[
    Evaluate[N[expr, wp]], {x, 0, 1},
    WorkingPrecision -> wp,
    AccuracyGoal -> Floor[0.38 wp],
    PrecisionGoal -> Floor[0.38 wp],
    MinRecursion -> 2,
    MaxRecursion -> 30,
    Method -> {"GlobalAdaptive", "SymbolicProcessing" -> 0}
  ]
];

phiN[ee_?NumericQ, wp_:WorkingPrecisionGoal] :=
  (psiN[ee, wp] - N[psi0Exact, wp])/8;

phiPrimeN[ee_?NumericQ, wp_:WorkingPrecisionGoal] := Which[
  TrueQ[ee == 0], N[phiPrime0Exact, wp],
  TrueQ[0 < ee < 1], Module[{ep = N[ee, wp], expr},
    expr = dHdeExpr /. e -> ep;
    NIntegrate[
      Evaluate[N[expr, wp]], {x, 0, 1},
      WorkingPrecision -> wp,
      AccuracyGoal -> Floor[0.34 wp],
      PrecisionGoal -> Floor[0.34 wp],
      MinRecursion -> 3,
      MaxRecursion -> 35,
      Method -> {"GlobalAdaptive", "SymbolicProcessing" -> 0}
    ]/8
  ],
  True, $Failed
];

(* ------------------------ moderate numerical audit ---------------------- *)

If[TrueQ[RunNumericalAudit],
  log["Running high-precision numerical audit..."];

  auditGrid = {
    0, 1/10000, 1/1000, 1/100, 1/10, 1/5,
    2/5, 1/2, 3/5, 4/5, 9/10, 49/50, 199/200, 999/1000
  };

  {auditSeconds, auditRows} = AbsoluteTiming[
    Table[
      Module[{pf, pt, ph, pairPhi, dp},
        pf = psiN[ee, WorkingPrecisionGoal];
        pt = psiTN[ee, WorkingPrecisionGoal];
        ph = psiHalfAngleN[ee, WorkingPrecisionGoal];
        pairPhi = (pf - N[psi0Exact, WorkingPrecisionGoal])/8;
        dp = phiPrimeN[ee, WorkingPrecisionGoal];
        {
          N[ee, 25], pf, pt, ph,
          Abs[pf - pt], Abs[pf - ph],
          pairPhi, dp
        }
      ],
      {ee, auditGrid}
    ]
  ];

  auditHeader = {
    "e", "psi_fixed", "psi_t", "psi_half_angle",
    "abs_fixed_minus_t", "abs_fixed_minus_half_angle",
    "phi", "phi_prime"
  };

  Export[
    FileNameJoin[{outputDirectory, "mathematica_numerical_scan.csv"}],
    Prepend[auditRows, auditHeader],
    "CSV"
  ];

  maxFormDiscrepancy = Max[Join[auditRows[[All, 5]], auditRows[[All, 6]]]];
  minSampledDerivative = Min[auditRows[[All, 8]]];
  meissnerReconstruction =
    N[2 Pi/3, WorkingPrecisionGoal] + 3 psiN[0, WorkingPrecisionGoal]/8;
  meissnerError = Abs[
    meissnerReconstruction - N[meissnerWidth1Exact, WorkingPrecisionGoal]
  ];

  log["Numerical audit seconds: " <> ToString[N[auditSeconds, 8]]];
  log["Maximum discrepancy among three exact integral forms: " <>
    ToString[N[maxFormDiscrepancy, 20], InputForm]];
  log["Minimum sampled Phi'(e): " <>
    ToString[N[minSampledDerivative, 20], InputForm]];
  log["Meissner reconstruction error: " <>
    ToString[N[meissnerError, 20], InputForm]];
  log["Exact Phi'(0): " <> ToString[N[phiPrime0Exact, 30], InputForm]];

  numericalAuditPass = TrueQ[
    maxFormDiscrepancy < 10^-30 &&
    meissnerError < 10^-30 &&
    minSampledDerivative > 0
  ];
  log["Moderate numerical audit pass: " <> ToString[numericalAuditPass]];
];

(* ---------------------- endpoint symbolic derivation -------------------- *)

If[TrueQ[RunEndpointSymbolics],
  log["Attempting exact endpoint derivative from the fixed-interval integrand..."];

  endpointSeriesCoefficient = TimeConstrained[
    Assuming[0 < x < 1,
      FullSimplify[SeriesCoefficient[hFixedExpr, {e, 0, 1}]]
    ],
    EndpointTimeLimitSeconds,
    $Aborted
  ];
  Put[
    endpointSeriesCoefficient,
    FileNameJoin[{outputDirectory, "endpoint_integrand_series_coefficient.wl"}]
  ];

  endpointDerivativeLimit = TimeConstrained[
    Assuming[0 < x < 1,
      FullSimplify[Limit[dHdeExpr, e -> 0, Direction -> "FromAbove"]]
    ],
    EndpointTimeLimitSeconds,
    $Aborted
  ];
  Put[
    endpointDerivativeLimit,
    FileNameJoin[{outputDirectory, "endpoint_integrand_derivative_limit.wl"}]
  ];

  endpointIntegrandAgreement = If[
    endpointSeriesCoefficient === $Aborted || endpointDerivativeLimit === $Aborted,
    $Aborted,
    TimeConstrained[
      Assuming[0 < x < 1,
        FullSimplify[endpointSeriesCoefficient - endpointDerivativeLimit]
      ],
      EndpointTimeLimitSeconds,
      $Aborted
    ]
  ];
  Put[
    endpointIntegrandAgreement,
    FileNameJoin[{outputDirectory, "endpoint_integrand_method_difference.wl"}]
  ];

  endpointIntegralResult = If[
    endpointSeriesCoefficient === $Aborted,
    $Aborted,
    TimeConstrained[
      FullSimplify[
        Integrate[
          endpointSeriesCoefficient,
          {x, 0, 1},
          GenerateConditions -> False
        ]/8
      ],
      EndpointTimeLimitSeconds,
      $Aborted
    ]
  ];
  Put[
    endpointIntegralResult,
    FileNameJoin[{outputDirectory, "endpoint_phi_prime_from_integral.wl"}]
  ];

  endpointClosedFormDifference = If[
    endpointIntegralResult === $Aborted,
    $Aborted,
    TimeConstrained[
      FullSimplify[endpointIntegralResult - phiPrime0Exact],
      EndpointTimeLimitSeconds,
      $Aborted
    ]
  ];
  Put[
    endpointClosedFormDifference,
    FileNameJoin[{outputDirectory, "endpoint_closed_form_difference.wl"}]
  ];

  log["Endpoint series-coefficient result status: " <>
    If[endpointSeriesCoefficient === $Aborted, "$Aborted", "completed"]];
  log["Endpoint derivative-limit result status: " <>
    If[endpointDerivativeLimit === $Aborted, "$Aborted", "completed"]];
  log["Endpoint integral result: " <> ToString[endpointIntegralResult, InputForm]];
  log["Difference from known exact Phi'(0): " <>
    ToString[endpointClosedFormDifference, InputForm]];
];

(* -------------------------- rapidity identity ---------------------------- *)

rapidityIdentity = FullSimplify[
  b2[Tanh[lam]] - Cosh[2 lam + 2 ArcSinh[1]],
  Assumptions -> lam >= 0
];
Put[
  rapidityIdentity,
  FileNameJoin[{outputDirectory, "rapidity_b2_identity_difference.wl"}]
];
log["Rapidity b^2 identity difference: " <> ToString[rapidityIdentity, InputForm]];

(* -------------------------- heavy symbolic mode -------------------------- *)

If[TrueQ[RunHeavySymbolics],
  log["HEAVY MODE: constructing rapidity derivative integrand..."];

  dHdLamRaw = (dHdeExpr /. e -> Tanh[lam]) Sech[lam]^2;
  Put[
    dHdLamRaw,
    FileNameJoin[{outputDirectory, "rapidity_derivative_integrand_raw.wl"}]
  ];

  dHdLamSimplified = TimeConstrained[
    FullSimplify[
      FunctionExpand[dHdLamRaw],
      Assumptions -> lam > 0 && 0 < x < 1
    ],
    HeavyTimeLimitSeconds,
    $Aborted
  ];
  Put[
    dHdLamSimplified,
    FileNameJoin[{outputDirectory, "rapidity_derivative_integrand_simplified.wl"}]
  ];
  log["HEAVY MODE: rapidity simplification status: " <>
    If[dHdLamSimplified === $Aborted, "$Aborted", "completed"]];

  derivativeForIntegration = If[
    dHdLamSimplified === $Aborted,
    dHdLamRaw,
    dHdLamSimplified
  ];

  directRapidityIntegral = TimeConstrained[
    FullSimplify[
      Integrate[
        derivativeForIntegration,
        {x, 0, 1},
        GenerateConditions -> False
      ]/8,
      Assumptions -> lam > 0
    ],
    HeavyTimeLimitSeconds,
    $Aborted
  ];
  Put[
    directRapidityIntegral,
    FileNameJoin[{outputDirectory, "direct_rapidity_phi_derivative_integral.wl"}]
  ];
  log["HEAVY MODE: direct rapidity integral result: " <>
    ToString[directRapidityIntegral, InputForm]];

  If[directRapidityIntegral =!= $Aborted,
    directRapiditySign = TimeConstrained[
      FullSimplify[directRapidityIntegral > 0, Assumptions -> lam > 0],
      HeavyTimeLimitSeconds,
      $Aborted
    ];
    Put[
      directRapiditySign,
      FileNameJoin[{outputDirectory, "direct_rapidity_phi_derivative_sign.wl"}]
    ];
    log["HEAVY MODE: direct rapidity sign result: " <>
      ToString[directRapiditySign, InputForm]];
  ];

  (*
    Integration-by-parts search.

    After differentiation the expression is linear in the single ArcTan
    appearing in angleX.  Write

        d/dlam h = P(lam,x) A(lam,x) + Q(lam,x),

    where A is that ArcTan.  If Mathematica finds J_x=P, then

        integral P A dx = [J A]_0^1 - integral J A_x dx.

    The resulting remainder Q-J A_x is exported for sign inspection.
  *)

  arcLam = angleX[Tanh[lam], x];
  collectedRapidity = TimeConstrained[
    Collect[Together[dHdLamRaw], arcLam, Together],
    HeavyTimeLimitSeconds,
    $Aborted
  ];
  Put[
    collectedRapidity,
    FileNameJoin[{outputDirectory, "rapidity_derivative_collected_in_arctan.wl"}]
  ];

  If[collectedRapidity =!= $Aborted,
    pCoefficient = TimeConstrained[
      FullSimplify[
        Coefficient[collectedRapidity, arcLam, 1],
        Assumptions -> lam > 0 && 0 < x < 1
      ],
      HeavyTimeLimitSeconds,
      $Aborted
    ];

    qRemainder = If[
      pCoefficient === $Aborted,
      $Aborted,
      TimeConstrained[
        FullSimplify[
          collectedRapidity - pCoefficient arcLam,
          Assumptions -> lam > 0 && 0 < x < 1
        ],
        HeavyTimeLimitSeconds,
        $Aborted
      ]
    ];

    Put[pCoefficient,
      FileNameJoin[{outputDirectory, "ibp_arctan_coefficient_P.wl"}]
    ];
    Put[qRemainder,
      FileNameJoin[{outputDirectory, "ibp_arctan_free_part_Q.wl"}]
    ];

    primitiveRaw = If[
      pCoefficient === $Aborted,
      $Aborted,
      TimeConstrained[
        Integrate[pCoefficient, x, GenerateConditions -> False],
        HeavyTimeLimitSeconds,
        $Aborted
      ]
    ];

    primitiveNormalized = If[
      primitiveRaw === $Aborted,
      $Aborted,
      TimeConstrained[
        FullSimplify[
          primitiveRaw - (primitiveRaw /. x -> 0),
          Assumptions -> lam > 0 && 0 <= x <= 1
        ],
        HeavyTimeLimitSeconds,
        $Aborted
      ]
    ];

    Put[primitiveRaw,
      FileNameJoin[{outputDirectory, "ibp_primitive_raw.wl"}]
    ];
    Put[primitiveNormalized,
      FileNameJoin[{outputDirectory, "ibp_primitive_normalized.wl"}]
    ];

    If[
      primitiveNormalized =!= $Aborted && qRemainder =!= $Aborted,

      ibpBoundary = TimeConstrained[
        FullSimplify[
          (primitiveNormalized arcLam /. x -> 1) -
          (primitiveNormalized arcLam /. x -> 0),
          Assumptions -> lam > 0
        ],
        HeavyTimeLimitSeconds,
        $Aborted
      ];

      ibpRemainder = TimeConstrained[
        FullSimplify[
          qRemainder - primitiveNormalized D[arcLam, x],
          Assumptions -> lam > 0 && 0 < x < 1
        ],
        HeavyTimeLimitSeconds,
        $Aborted
      ];

      Put[ibpBoundary,
        FileNameJoin[{outputDirectory, "ibp_boundary_term.wl"}]
      ];
      Put[ibpRemainder,
        FileNameJoin[{outputDirectory, "ibp_remainder_after_parts.wl"}]
      ];

      ibpRemainderSign = If[
        ibpRemainder === $Aborted,
        $Aborted,
        TimeConstrained[
          FullSimplify[
            ibpRemainder >= 0,
            Assumptions -> lam > 0 && 0 < x < 1
          ],
          HeavyTimeLimitSeconds,
          $Aborted
        ]
      ];
      Put[ibpRemainderSign,
        FileNameJoin[{outputDirectory, "ibp_remainder_sign_test.wl"}]
      ];

      log["HEAVY MODE: IBP primitive status: completed"];
      log["HEAVY MODE: IBP boundary term: " <>
        ToString[ibpBoundary, InputForm]];
      log["HEAVY MODE: IBP remainder sign test: " <>
        ToString[ibpRemainderSign, InputForm]];
      ,
      log["HEAVY MODE: IBP search did not obtain a usable primitive/remainder."]
    ];
  ];
];

(* ------------------------------ final report ----------------------------- *)

summaryAssociation = <|
  "MathematicaVersion" -> $Version,
  "RunNumericalAudit" -> RunNumericalAudit,
  "RunEndpointSymbolics" -> RunEndpointSymbolics,
  "RunHeavySymbolics" -> RunHeavySymbolics,
  "WorkingPrecisionGoal" -> WorkingPrecisionGoal,
  "MeissnerWidth1Exact" -> ToString[meissnerWidth1Exact, InputForm],
  "MeissnerWidth1Numeric50" -> ToString[N[meissnerWidth1Exact, 50], InputForm],
  "Psi0Exact" -> ToString[psi0Exact, InputForm],
  "PhiPrime0Exact" -> ToString[phiPrime0Exact, InputForm],
  "PhiPrime0Numeric50" -> ToString[N[phiPrime0Exact, 50], InputForm],
  "RapidityIdentityDifference" -> ToString[rapidityIdentity, InputForm]
|>;

If[ValueQ[numericalAuditPass],
  summaryAssociation = Append[
    summaryAssociation,
    "NumericalAuditPass" -> numericalAuditPass
  ]
];
If[ValueQ[endpointClosedFormDifference],
  summaryAssociation = Append[
    summaryAssociation,
    "EndpointClosedFormDifference" ->
      ToString[endpointClosedFormDifference, InputForm]
  ]
];

Put[
  summaryAssociation,
  FileNameJoin[{outputDirectory, "mathematica_summary.wl"}]
];
Export[
  FileNameJoin[{outputDirectory, "mathematica_summary.json"}],
  summaryAssociation,
  "RawJSON"
];

log["CONFOCAL PEABODY MATHEMATICA AUDIT: COMPLETE"];
Close[reportStream];

summaryAssociation
