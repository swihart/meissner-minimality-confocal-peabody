#!/usr/bin/env python3
"""Semantic and deterministic validation of the Peabody family theorem package."""
from __future__ import annotations
import contextlib, hashlib, io, json, tempfile, zipfile, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'python'))
import peabody_central_interval_certificate as cert

def sha256(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 return h.hexdigest()

def strip_core(d):
 bulk=dict(d['bulk']);bulk.pop('elapsed_seconds',None)
 return {'certificate_version':d['certificate_version'],'formula_version':d['formula_version'],'interval_precision_decimal_digits':d['interval_precision_decimal_digits'],'local_endpoint':d['local_endpoint'],'bulk':bulk,'global_domain_diagnostics':d['global_domain_diagnostics'],'new_central_terminal_boxes':d['new_central_terminal_boxes'],'proof_status':d['proof_status'],'classification':d['classification']}

def main():
 checks={}
 # Portable checksums.
 bad=[]
 for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
  if not line.strip():continue
  digest,rel=line.split('  ',1);p=ROOT/rel
  if not p.is_file() or sha256(p)!=digest:bad.append(rel)
 checks['sha256_pass']=not bad;checks['sha256_failures']=bad
 central=json.loads((ROOT/'certificates/peabody_central_certificate.json').read_text())
 family=json.loads((ROOT/'certificates/peabody_family_certificate.json').read_text())
 ca=json.loads((ROOT/'data/central_certificate_adversarial_audit.json').read_text())
 aa=json.loads((ROOT/'data/additivity_audit.json').read_text())
 checks['central_classification_pass']=central['classification']=='GO_PEABODY_CENTRAL_PHI_POSITIVITY_CERTIFIED'
 checks['family_classification_pass']=family['principal_classification']=='GO_PEABODY_FAMILY_MINIMALITY_CERTIFIED' and family['proof_status']=='CERTIFIED'
 checks['central_audit_pass']=ca['audit_pass'] is True
 checks['additivity_audit_pass']=aa['audit_pass'] is True
 checks['box_accounting_pass']=central['new_central_terminal_boxes']==590 and family['combined_terminal_boxes']==2590
 checks['scope_discipline_pass']=all(family['claim_discipline'].values())
 # Frozen dependency ZIP semantics.
 tailzip=ROOT/'frozen_inputs/confocal_peabody_tail_first_gate_2026-09-30.zip'
 with zipfile.ZipFile(tailzip) as z:
  name=next(n for n in z.namelist() if n.endswith('data/certificate_80dps/tail_certificate.json'))
  tail=json.loads(z.read(name))
 checks['tail_zip_semantic_pass']=tail['classification']=='GO_PEABODY_TAIL_PHI_POSITIVITY_CERTIFIED'
 v4zip=ROOT/'frozen_inputs/confocal_peabody_v4_validated_checkpoint_2026-09-30.zip'
 with zipfile.ZipFile(v4zip) as z:
  name=next(n for n in z.namelist() if n.endswith('data/validated_output_summary.json'))
  v4=json.loads(z.read(name))
 checks['v4_zip_semantic_pass']=v4['required_campaign_gates_pass'] is True and v4['checks']['optional_fixed_rho_integrate_evaluated'] is False
 # Deterministic central proof-core replay.
 with tempfile.TemporaryDirectory() as td:
  out=Path(td)/'central'
  # Suppress the certifier's verbose certificate dump so this validator's
  # transcript is deterministic and contains only the semantic validation.
  with contextlib.redirect_stdout(io.StringIO()):
   fresh=cert.run(out,80,'bfs',False)
  freshd=json.loads((out/'peabody_central_certificate.json').read_text())
  a=json.dumps(strip_core(central),sort_keys=True,separators=(',',':'))
  b=json.dumps(strip_core(freshd),sort_keys=True,separators=(',',':'))
  checks['clean_central_replay_pass']=a==b
  checks['archived_proof_core_sha256']=hashlib.sha256(a.encode()).hexdigest()
  checks['replayed_proof_core_sha256']=hashlib.sha256(b.encode()).hexdigest()
 required=['sha256_pass','central_classification_pass','family_classification_pass','central_audit_pass','additivity_audit_pass','box_accounting_pass','scope_discipline_pass','tail_zip_semantic_pass','v4_zip_semantic_pass','clean_central_replay_pass']
 passed=all(bool(checks[k]) for k in required)
 result={'validation_pass':passed,'required_checks':required,'checks':checks,'classification':'PEABODY_FAMILY_PACKAGE_VALIDATION_PASS' if passed else 'PEABODY_FAMILY_PACKAGE_VALIDATION_FAIL'}
 (ROOT/'data/package_validation.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2));raise SystemExit(0 if passed else 1)
if __name__=='__main__':main()
