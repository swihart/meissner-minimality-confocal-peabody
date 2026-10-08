(* ::Package:: *)

(* Recursive unresolved-expression guard for the Peabody release audit. *)

ClearAll[
  PeabodyGuardReadHeld,
  PeabodyGuardFile,
  PeabodyGuardTree,
  PeabodyGuardForbiddenSymbols,
  PeabodyGuardUnresolvedHeads,
  PeabodyGuardPlaceholderSymbols
];

PeabodyGuardForbiddenSymbols = {
  $Aborted, $Failed, Indeterminate, ComplexInfinity, Undefined
};

PeabodyGuardUnresolvedHeads = {
  Integrate, NIntegrate, Reduce, Resolve, FindInstance
};

PeabodyGuardReadHeld[path_String] := Quiet@Check[
  ToExpression[Import[path, "Text"], InputForm, HoldComplete],
  $Failed
];

PeabodyGuardFile[path_String, allowIntegrate_:False] := Module[
  {held, forbidden, unresolved, placeholders, text, pass},
  text = Import[path, "Text"];
  held = PeabodyGuardReadHeld[path];
  If[held === $Failed,
    Return[<|
      "Path" -> path,
      "ParsePass" -> False,
      "Pass" -> False,
      "Reason" -> "ToExpression[...,HoldComplete] failed"
    |>]
  ];

  forbidden = DeleteDuplicates@Cases[
    held,
    s_Symbol /; MemberQ[PeabodyGuardForbiddenSymbols, Unevaluated[s]],
    Infinity
  ];

  unresolved = DeleteDuplicates@Cases[
    held,
    expression_ /; MemberQ[
      PeabodyGuardUnresolvedHeads,
      Quiet@Check[Head[Unevaluated[expression]], None]
    ],
    Infinity
  ];

  If[TrueQ[allowIntegrate],
    unresolved = DeleteCases[unresolved, _Integrate]
  ];

  placeholders = DeleteDuplicates@Cases[
    held,
    s_Symbol /; StringMatchQ[SymbolName[Unevaluated[s]], ___ ~~ "Expr"],
    Infinity
  ];

  pass = forbidden === {} && unresolved === {} && placeholders === {};
  <|
    "Path" -> path,
    "Bytes" -> FileByteCount[path],
    "ParsePass" -> True,
    "AllowIntegrate" -> TrueQ[allowIntegrate],
    "ForbiddenSymbols" -> (ToString[#, InputForm] & /@ forbidden),
    "UnresolvedExpressions" -> (ToString[#, InputForm] & /@ unresolved),
    "PlaceholderSymbols" -> (ToString[#, InputForm] & /@ placeholders),
    "TextContainsAborted" -> StringContainsQ[text, "$Aborted"],
    "Pass" -> pass
  |>
];

PeabodyGuardTree[root_String] := Module[
  {files, optionalSuffix, rows},
  optionalSuffix = FileNameJoin[{
    "mathematica_output_primitive_probe_v4",
    "rt_sector_fixed_rho_primitive.wl"
  }];
  files = Sort@FileNames["*.wl", root, Infinity];
  rows = PeabodyGuardFile[
      #,
      StringEndsQ[#, optionalSuffix]
    ] & /@ files;
  <|
    "Root" -> root,
    "FileCount" -> Length[rows],
    "Files" -> rows,
    "Pass" -> And @@ Lookup[rows, "Pass", False]
  |>
];
