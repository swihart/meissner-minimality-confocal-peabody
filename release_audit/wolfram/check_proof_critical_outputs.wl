(* ::Package:: *)

ClearAll["Global`*"];
$HistoryLength = 0;

scriptDirectory = DirectoryName[ExpandFileName[$InputFileName]];
Get[FileNameJoin[{scriptDirectory, "recursive_unresolved_guard.wl"}]];

outputRoot = Environment["PEABODY_WOLFRAM_OUTPUT_ROOT"];
summaryPath = Environment["PEABODY_WOLFRAM_GUARD_JSON"];
If[! StringQ[outputRoot] || ! DirectoryQ[outputRoot],
  Print["FATAL: PEABODY_WOLFRAM_OUTPUT_ROOT is not a directory."];
  Quit[2]
];
If[! StringQ[summaryPath] || StringLength[summaryPath] == 0,
  Print["FATAL: PEABODY_WOLFRAM_GUARD_JSON is unset."];
  Quit[2]
];

componentSummary = Import[
  FileNameJoin[{outputRoot, "mathematica_output_component_diagnostic_v4", "component_diagnostic_summary.json"}],
  "RawJSON"
];
compressedSummary = Import[
  FileNameJoin[{outputRoot, "mathematica_output_compressed_audit_v4", "compressed_audit_summary.json"}],
  "RawJSON"
];
primitiveSummary = Import[
  FileNameJoin[{outputRoot, "mathematica_output_primitive_probe_v4", "primitive_probe_summary.json"}],
  "RawJSON"
];
intervalSummary = Import[
  FileNameJoin[{outputRoot, "mathematica_output_interval_inputs_v4", "interval_input_summary.json"}],
  "RawJSON"
];

summaryGate = TrueQ[componentSummary["Pass"]] &&
  TrueQ[compressedSummary["Pass"]] &&
  TrueQ[primitiveSummary["ExactLowComplexityObstructionPass"]] &&
  TrueQ[intervalSummary["NumericalScoutPass"]] &&
  intervalSummary["ProofStatus"] === "NOT_CERTIFIED";

treeAudit = PeabodyGuardTree[outputRoot];
optionalPrimitivePath = FileNameJoin[{
  outputRoot,
  "mathematica_output_primitive_probe_v4",
  "rt_sector_fixed_rho_primitive.wl"
}];
optionalHeld = PeabodyGuardReadHeld[optionalPrimitivePath];
optionalIntegratePresent = optionalHeld =!= $Failed &&
  Cases[optionalHeld, _Integrate, Infinity] =!= {};

pass = summaryGate && TrueQ[treeAudit["Pass"]] && optionalIntegratePresent;
result = <|
  "Classification" -> If[
    pass,
    "PEABODY_WOLFRAM_RECURSIVE_GUARD_PASS",
    "PEABODY_WOLFRAM_RECURSIVE_GUARD_FAIL"
  ],
  "Pass" -> pass,
  "MathematicaVersion" -> $Version,
  "OutputRoot" -> outputRoot,
  "SummaryGate" -> summaryGate,
  "OptionalFixedRhoIntegratePresent" -> optionalIntegratePresent,
  "OptionalFixedRhoIntegrateIsProofAuthority" -> False,
  "TreeAudit" -> treeAudit,
  "ComponentSummary" -> componentSummary,
  "CompressedSummary" -> compressedSummary,
  "PrimitiveSummary" -> primitiveSummary,
  "IntervalSummary" -> intervalSummary
|>;

CreateDirectory[DirectoryName[summaryPath], CreateIntermediateDirectories -> True];
Export[summaryPath, result, "RawJSON"];
Print[result];
Quit[If[pass, 0, 1]];
