(* Independent semantic audit for the Peabody analytical-compression lemma.
   Not proof authority.  Uses fresh exact definitions and finite high-precision
   checks only; it does not launch unrestricted Integrate or FullSimplify. *)

ClearAll["Global`*"];

workingPrecision = 100;
timeLimit = 300;

kappa = 1 + Sqrt[2];
K = kappa^2;
psi0 = -(2 Pi/Sqrt[3]) ArcCos[1/3];

ClearAll[h, q, x];
h[q_, x_] := Module[{D0, R0, T0, delta, M, p1, p2, q0, z},
  D0 = Sqrt[K^2 + q^2];
  R0 = Sqrt[K^2 + q^2 - 2 K q x^2];
  T0 = Sqrt[2 K (K^2 + q^2) + K^2 (1 - q)^2 x^2];
  delta = 2 K (1 - x^2)/(R0 + K - q);
  M = K (q - 2 K x^2)/(R0 + K) + (1 - K) R0 - K^2 - q R0 - q - q^2;
  p1 = -16 Sqrt[2] kappa (K^2 + q^2)/(R0 T0);
  p2 = -4 K (1 - q^2) (K^2 + q^2) delta M/(R0 T0^3);
  q0 = -4 K (1 - q^2) (K^2 + q^2) delta/(R0 T0^2);
  z = K ((1 + q) D0 + (1 - q) R0)/(T0 (K + q + D0));
  (p1 + p2) ArcTan[z] + q0
];

endpointH[x_] := Module[{A = 2 K + x^2},
  (-16 Sqrt[2] kappa/Sqrt[A] + 4 (1 - x^2) (A - 1)/A^(3/2)) ArcTan[1/Sqrt[A]]
  - 4 (1 - x^2)/A
];

endpointDifference = TimeConstrained[
  Together[FunctionExpand[h[0, x] - endpointH[x]]],
  timeLimit,
  $Aborted
];

phiOne = NIntegrate[
  endpointH[x], {x, 0, 1},
  WorkingPrecision -> workingPrecision,
  AccuracyGoal -> 70,
  PrecisionGoal -> 70,
  Method -> {"GlobalAdaptive", "SymbolicProcessing" -> 0}
]/8 - N[psi0/8, workingPrecision];

hq = D[h[q, x], q];
hqq = D[h[q, x], {q, 2}];
phiSecondAtQ[q0_?NumericQ] := N[(1 + q0)^3/32 NIntegrate[
  ((1 + q) hqq + 2 hq) /. q -> q0,
  {x, 0, 1},
  WorkingPrecision -> workingPrecision,
  AccuracyGoal -> 55,
  PrecisionGoal -> 55,
  Method -> {"GlobalAdaptive", "SymbolicProcessing" -> 0}
], 60];

qSamples = Rationalize[Range[1, 63, 10]/64, 0];
secondSamples = Association@Table[
  ToString[q0, InputForm] -> phiSecondAtQ[N[q0, workingPrecision]],
  {q0, qSamples}
];

containsUnresolved[expr_] := ! FreeQ[HoldComplete[expr],
  _Integrate | _NIntegrate | _FullSimplify | _Simplify | _D,
  Infinity
];

endpointPass = TrueQ[phiOne > 3/10000];
secondPass = And @@ (TrueQ[# < -1/25000] & /@ Values[secondSamples]);
endpointFormulaPass = endpointDifference === 0;
unresolvedPass = ! containsUnresolved[phiOne] && ! containsUnresolved[secondSamples];
pass = endpointPass && secondPass && endpointFormulaPass && unresolvedPass;

result = <|
  "audit_version" -> "PEABODY_ANALYTIC_COMPRESSION_WOLFRAM_SEMANTIC_V1",
  "classification" -> If[pass,
    "PEABODY_ANALYTIC_COMPRESSION_WOLFRAM_SEMANTIC_PASS",
    "PEABODY_ANALYTIC_COMPRESSION_WOLFRAM_SEMANTIC_FAIL"],
  "pass" -> pass,
  "proof_authority" -> False,
  "endpoint_formula_difference" -> ToString[endpointDifference, InputForm],
  "phi_one" -> ToString[phiOne, InputForm],
  "endpoint_pass" -> endpointPass,
  "second_derivative_samples" -> Map[ToString[#, InputForm] &, secondSamples],
  "second_derivative_pass" -> secondPass,
  "recursive_unresolved_guard_pass" -> unresolvedPass
|>;

baseDirectory = Quiet@Check[DirectoryName[$InputFileName], Directory[]];
If[! StringQ[baseDirectory] || StringLength[baseDirectory] == 0, baseDirectory = Directory[]];
outputPath = FileNameJoin[{baseDirectory, "peabody_concavity_semantic_audit.json"}];
Export[outputPath, result, "RawJSON"];
Print[result];
Print[If[pass,
  "PEABODY_ANALYTIC_COMPRESSION_WOLFRAM_SEMANTIC_PASS",
  "PEABODY_ANALYTIC_COMPRESSION_WOLFRAM_SEMANTIC_FAIL"]];
If[! pass, Exit[1]];
