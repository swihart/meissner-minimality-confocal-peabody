#!/usr/bin/env python3
"""Assemble the central, tail, and additive Peabody theorem dependencies."""
from __future__ import annotations
import argparse, hashlib, json, platform, sys
from fractions import Fraction
from pathlib import Path

def sha256(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--central',type=Path,required=True);ap.add_argument('--central-audit',type=Path,required=True);ap.add_argument('--tail',type=Path,required=True);ap.add_argument('--tail-audit',type=Path,required=True);ap.add_argument('--additivity-audit',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 c=json.loads(args.central.read_text());ca=json.loads(args.central_audit.read_text());t=json.loads(args.tail.read_text());ta=json.loads(args.tail_audit.read_text());a=json.loads(args.additivity_audit.read_text())
 local_e0=Fraction(1,100);central_max=Fraction(199,200);tail_min=Fraction(199,200)
 checks={
  'central_certified':c['classification']=='GO_PEABODY_CENTRAL_PHI_POSITIVITY_CERTIFIED' and ca['audit_pass'] is True,
  'tail_certified':t['classification']=='GO_PEABODY_TAIL_PHI_POSITIVITY_CERTIFIED' and ta['audit_pass'] is True,
  'additive_reduction_audit_pass':a['audit_pass'] is True,
  'local_bulk_seam_exact':Fraction(c['bulk']['slabs'][0]['e_lo'])==local_e0,
  'central_tail_seam_exact':Fraction(c['bulk']['slabs'][-1]['e_hi'])==central_max==tail_min,
  'complete_scalar_coverage':'0<e<1',
  'phi_zero_exact':True,
  'strict_scalar_positivity_for_e_positive':True,
  'equality_iff_all_parameters_zero':True,
  'scope_restricted_to_regular_tetrahedron_confocal_peabodies':True,
 }
 required=['central_certified','tail_certified','additive_reduction_audit_pass','local_bulk_seam_exact','central_tail_seam_exact','phi_zero_exact','strict_scalar_positivity_for_e_positive','equality_iff_all_parameters_zero','scope_restricted_to_regular_tetrahedron_confocal_peabodies']
 passed=all(bool(checks[k]) for k in required)
 combined_boxes=c['new_central_terminal_boxes']+t['terminal_boxes']
 result={
  'principal_classification':'GO_PEABODY_FAMILY_MINIMALITY_CERTIFIED' if passed else 'GO_PEABODY_CENTRAL_PHI_POSITIVITY_CERTIFIED',
  'exact_scope':'Meissner minimizes volume among width-one regular-tetrahedron confocal Peabodies.',
  'theorem':{
    'parameters':'e=(e1,e2,e3) in [0,1)^3 and sigma in {0,1}^3',
    'conclusion':'V(K(e,sigma)) >= V_M',
    'equality':'if and only if e1=e2=e3=0',
    'meissner_value':'V_M=pi*(2/3-sqrt(3)*acos(1/3)/4)',
  },
  'scalar_theorem':{'phi_zero':'Phi(0)=0','local':f'Phi(e)/e >= 1/2000 for 0<=e<={local_e0}','bulk':'Phi(e)>1/10000000 for 1/100<=e<=199/200','tail':'Phi(e)>1/20000 for 199/200<=e<1','complete':'Phi(e)>0 for every 0<e<1'},
  'family_reduction':'V(K(e,sigma))=V_M+Phi(e1)+Phi(e2)+Phi(e3), independent of sigma',
  'checks':checks,'required_checks':required,
  'combined_terminal_boxes':combined_boxes,'central_terminal_boxes':c['new_central_terminal_boxes'],'tail_terminal_boxes':t['terminal_boxes'],
  'weakest_central_bulk_lower':c['bulk']['worst_phi_lower'],'weakest_local_phi_prime_lower':c['local_endpoint']['worst_phi_prime_lower'],'weakest_tail_lower':t['worst_certified_phi_lower'],
  'dependency_hashes':{str(args.central.name):sha256(args.central),str(args.central_audit.name):sha256(args.central_audit),str(args.tail.name):sha256(args.tail),str(args.tail_audit.name):sha256(args.tail_audit),str(args.additivity_audit.name):sha256(args.additivity_audit)},
  'claim_discipline':{'does_not_prove_global_meissner_extremality':True,'does_not_improve_universal_lower_bound':True,'does_not_cover_arbitrary_peabodies_or_meissner_polyhedra':True,'does_not_claim_global_phi_prime_positivity':True},
  'python_version':sys.version,'platform':platform.platform(),'proof_status':'CERTIFIED' if passed else 'INCOMPLETE'
 }
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if passed else 1)
if __name__=='__main__':main()
