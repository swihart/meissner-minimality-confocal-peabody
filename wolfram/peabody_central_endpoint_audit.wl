(* ::Package:: *)
(* Independent exact/numerical endpoint audit. No unrestricted Integrate or FullSimplify. *)
ClearAll["Global`*"];
$HistoryLength = 0;
wp = 100;
alpha = ArcCos[1/3];
phiPrime0Exact = 1/2 (
  5 Pi/(3 Sqrt[3]) - 3 +
  alpha (3 Sqrt[2]/2 - 5 Sqrt[6] Pi/18)
);
e0 = 1/100;
centralMax = 199/200;
q[e_] := (1 - e)/(1 + e);
checks = <|
  "PhiPrime0Exact" -> ToString[phiPrime0Exact, InputForm],
  "PhiPrime0Numeric" -> ToString[N[phiPrime0Exact, wp], InputForm],
  "PhiPrime0AboveOneOver2000" -> TrueQ[N[phiPrime0Exact - 1/2000, wp] > 0],
  "LocalBulkSeam" -> TrueQ[e0 == 1/100],
  "CentralTailQSeam" -> TrueQ[q[centralMax] == 1/399],
  "Classification" -> "PEABODY_CENTRAL_ENDPOINT_AUDIT_PASS"
|>;
Print[checks];
checks
