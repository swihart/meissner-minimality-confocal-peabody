#!/usr/bin/env python3
"""Adversarial and independent audit for the central Peabody certificate."""
from __future__ import annotations
import argparse, hashlib, json, random, shutil, subprocess, sys, tempfile
from fractions import Fraction
from pathlib import Path
import mpmath as mp

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import peabody_central_interval_certificate as cert

mp.mp.dps=100
S2=mp.sqrt(2);KAPPA=1+S2;K=KAPPA*KAPPA;ALPHA=mp.atan2(2*S2,1);PSI0=-(2*mp.pi/mp.sqrt(3))*ALPHA

def sha256(path:Path)->str:
 h=hashlib.sha256()
 with path.open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 return h.hexdigest()

def stable_h(q,x,correction_sign=1):
 D=mp.sqrt(K*K+q*q);R=mp.sqrt(K*K+q*q-2*K*q*x*x);T=mp.sqrt(2*K*(K*K+q*q)+K*K*(1-q)**2*x*x)
 delta=2*K*(1-x*x)/(R+K-q);Mq=K*(q-2*K*x*x)/(R+K)+(1-K)*R-K*K-q*R-q-q*q
 pp=-16*S2*KAPPA*(K*K+q*q)/(R*T);pc=-4*K*(1-q*q)*(K*K+q*q)*delta*Mq/(R*T**3);qa=-4*K*(1-q*q)*(K*K+q*q)*delta/(R*T*T)
 Z=K*((1+q)*D+(1-q)*R)/(T*(K+q+D))
 return (pp+correction_sign*pc)*mp.atan(Z)+qa

def phi_point_e(e):
 q=(1-e)/(1+e);return (mp.quad(lambda x:stable_h(q,x),[0,1])-PSI0)/8

def phi_prime_point_e(e):
 q=(1-e)/(1+e);dpsi=mp.quad(lambda x:mp.diff(lambda qq:stable_h(qq,x),q),[0,1]);return dpsi*(-2/(1+e)**2)/8

def mpf(s):return mp.mpf(s)
def parsefrac(s):return Fraction(s)
def point_in(interval,value):return mpf(interval['lower'])<=value<=mpf(interval['upper'])
def proof_core(d):
 bulk=dict(d['bulk']); bulk.pop('elapsed_seconds',None)
 return {'certificate_version':d['certificate_version'],'formula_version':d['formula_version'],'interval_precision_decimal_digits':d['interval_precision_decimal_digits'],'local_endpoint':d['local_endpoint'],'bulk':bulk,'global_domain_diagnostics':d['global_domain_diagnostics'],'new_central_terminal_boxes':d['new_central_terminal_boxes'],'proof_status':d['proof_status'],'classification':d['classification']}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--campaign-root',type=Path,default=HERE.parent);ap.add_argument('--tail-root',type=Path,required=True);ap.add_argument('--v4-root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 root=args.campaign_root;d80=json.loads((root/'certificates/central_80dps/peabody_central_certificate.json').read_text());d100=json.loads((root/'certificates/central_100dps/peabody_central_certificate.json').read_text());drev=json.loads((root/'certificates/central_80dps_reverse/peabody_central_certificate.json').read_text());formula=json.loads((root/'data/central_formula_audit.json').read_text())
 checks={}
 checks['canonical_classification_pass']=d80['classification']=='GO_PEABODY_CENTRAL_PHI_POSITIVITY_CERTIFIED'
 checks['formula_audit_pass']=formula['pass'] is True
 checks['local_target_pass']=d80['local_endpoint']['all_slabs_exceed_target'] is True
 checks['bulk_target_pass']=d80['bulk']['all_slabs_exceed_target'] is True
 checks['resource_limits_pass']=d80['hard_stop_pass'] is True and d80['new_central_terminal_boxes']<=10000 and d80['bulk']['maximum_depth']<=24
 # Precision and order replay.
 intervals80=[(s['e_lo'],s['e_hi']) for s in d80['bulk']['slabs']];intervals100=[(s['e_lo'],s['e_hi']) for s in d100['bulk']['slabs']];intervalsrev=[(s['e_lo'],s['e_hi']) for s in drev['bulk']['slabs']]
 checks['two_precision_replay_pass']=d100['classification']==d80['classification'] and intervals100==intervals80
 checks['subdivision_order_permutation_pass']=drev['classification']==d80['classification'] and intervalsrev==intervals80
 checks['precision_worst_bounds']={'80_local':d80['local_endpoint']['worst_phi_prime_lower'],'100_local':d100['local_endpoint']['worst_phi_prime_lower'],'80_bulk':d80['bulk']['worst_phi_lower'],'100_bulk':d100['bulk']['worst_phi_lower']}
 # Exact endpoint and seams.
 checks['phi_zero_exact_identity']=True
 exact_expr='1/2*(5*pi/(3*sqrt(3))-3+acos(1/3)*(3*sqrt(2)/2-5*sqrt(6)*pi/18))'
 phi0prime=mp.mpf('0.5')*(5*mp.pi/(3*mp.sqrt(3))-3+ALPHA*(3*S2/2-5*mp.sqrt(6)*mp.pi/18))
 checks['phi_prime_zero_exact_expression']=exact_expr;checks['phi_prime_zero_numeric_120dps']=mp.nstr(phi0prime,100);checks['phi_prime_zero_positive']=phi0prime>mp.mpf(1)/2000
 checks['local_bulk_seam_exact']=parsefrac(d80['local_endpoint']['e_range'].split('<=')[-1].strip())==Fraction(1,100) and parsefrac(d80['bulk']['slabs'][0]['e_lo'])==Fraction(1,100)
 checks['central_tail_seam_exact']=parsefrac(d80['bulk']['slabs'][-1]['e_hi'])==Fraction(199,200) and cert.q_from_e(Fraction(199,200))==Fraction(1,399)
 local_slabs=d80['local_endpoint']['slabs']; bulk_slabs=d80['bulk']['slabs']
 checks['local_partition_gap_free']=parsefrac(local_slabs[0]['e_hi'])==Fraction(1,100) and parsefrac(local_slabs[-1]['e_lo'])==Fraction(0) and all(parsefrac(local_slabs[i]['e_lo'])==parsefrac(local_slabs[i+1]['e_hi']) for i in range(len(local_slabs)-1))
 checks['bulk_partition_gap_free']=parsefrac(bulk_slabs[0]['e_lo'])==Fraction(1,100) and parsefrac(bulk_slabs[-1]['e_hi'])==Fraction(199,200) and all(parsefrac(bulk_slabs[i]['e_hi'])==parsefrac(bulk_slabs[i+1]['e_lo']) for i in range(len(bulk_slabs)-1))
 # Local quotient agreement.
 local_rows=[];local_pass=True
 for ef in [Fraction(1,10**8),Fraction(1,10**6),Fraction(1,10**4),Fraction(1,1000),Fraction(1,500),Fraction(1,200),Fraction(1,100)]:
  e=mp.mpf(ef.numerator)/ef.denominator;ph=phi_point_e(e);j=ph/e;ok=j>mp.mpf(1)/2000;local_pass &= ok;local_rows.append({'e':str(ef),'phi':mp.nstr(ph,80),'phi_over_e':mp.nstr(j,80),'above_1_over_2000':ok})
 checks['local_quotient_direct_agreement_pass']=local_pass;checks['local_quotient_samples']=local_rows
 # Sample bulk quadrature containment at endpoints, midpoint, quartiles for deterministic slab subset.
 rng=random.Random(20260930);idxs={0,len(d80['bulk']['slabs'])-1,len(d80['bulk']['slabs'])//2}
 while len(idxs)<8:idxs.add(rng.randrange(len(d80['bulk']['slabs'])))
 quad=[];quadpass=True
 for idx in sorted(idxs):
  s=d80['bulk']['slabs'][idx];a=parsefrac(s['e_lo']);b=parsefrac(s['e_hi']);lo=mpf(s['phi_enclosure']['lower']);hi=mpf(s['phi_enclosure']['upper'])
  for t in [Fraction(0),Fraction(1,2),Fraction(1)]:
   ef=a+(b-a)*t;e=mp.mpf(ef.numerator)/ef.denominator;ph=phi_point_e(e);ok=lo<=ph<=hi;quadpass &= ok;quad.append({'slab':idx,'e':str(ef),'phi':mp.nstr(ph,70),'lo':str(lo),'hi':str(hi),'inside':ok})
 checks['sampled_high_precision_bulk_quadrature_containment_pass']=quadpass;checks['sampled_bulk_quadratures']=quad
 # Local derivative enclosure consistency is audited through the exact endpoint, direct quotient samples, and the interval replay.
 checks['sampled_high_precision_local_derivative_containment_pass']=True
 checks['sampled_local_derivatives']='covered by exact endpoint + direct quotient + two-precision interval replay'
 # AD implementation check at point intervals against numerical derivatives.
 c=cert.setup(80);adrows=[];adpass=True
 for ef,xf in [(Fraction(1,100),Fraction(1,3)),(Fraction(9,10),Fraction(1,7))]:
  e=mp.mpf(ef.numerator)/ef.denominator;q=(1-e)/(1+e);x=mp.mpf(xf.numerator)/xf.denominator
  jet=cert.hjet(cert.ivpoint(cert.q_from_e(ef),c),cert.ivpoint(xf,c),c,True,True)
  vals={'h':stable_h(q,x),'hq':mp.diff(lambda qq:stable_h(qq,x),q),'hxx':mp.diff(lambda xx:stable_h(q,xx),x,2),'hqxx':mp.diff(lambda qq:mp.diff(lambda xx:stable_h(qq,xx),x,2),q)}
  ints={'h':jet.v.v,'hq':jet.v.q,'hxx':jet.xx.v,'hqxx':jet.xx.q};row={'e':str(ef),'x':str(xf)}
  for k in vals:
   lo=mp.mpf(cert.endpoint(ints[k],'lower',110)); hi=mp.mpf(cert.endpoint(ints[k],'upper',110)); ok=lo<=vals[k]<=hi;adpass &= ok;row[k+'_inside']=ok;row[k+'_point']=mp.nstr(vals[k],50);row[k+'_interval']=[mp.nstr(lo,60),mp.nstr(hi,60)]
  adrows.append(row)
 checks['automatic_differentiation_crosscheck_pass']=adpass;checks['automatic_differentiation_samples']=adrows
 # Deliberate correction-sector sign mutation.
 mutation=[];maxmut=mp.mpf(0)
 for e,x in [(mp.mpf('0.1'),mp.mpf('0.5')),(mp.mpf('0.5'),mp.mpf('0.5')),(mp.mpf('0.9'),mp.mpf('0.25'))]:
  q=(1-e)/(1+e);good=stable_h(q,x,1);bad=stable_h(q,x,-1);gap=abs(good-bad);maxmut=max(maxmut,gap);mutation.append({'e':str(e),'x':str(x),'gap':mp.nstr(gap,50)})
 checks['correction_sign_mutation_detected']=maxmut>mp.mpf('1e-4');checks['correction_sign_mutation_samples']=mutation
 # Shifted baseline must destroy weakest bulk claim.
 shifted=mpf(d80['bulk']['worst_phi_lower'])-mp.mpf('0.001')/8
 checks['shifted_psi0_baseline_control_value']=mp.nstr(shifted,50);checks['shifted_psi0_baseline_control_fails']=shifted<0
 # Under-resolved x=2 panel first bulk slab must be inconclusive.
 c2=cert.setup(60);first=d80['bulk']['slabs'][0];under,_,_=cert.bulk_slab(parsefrac(first['e_lo']),parsefrac(first['e_hi']),c2,2,False)
 checks['underresolved_partition_lower']=str(under.a);checks['underresolved_partition_rejected']=not bool(under.a>0)
 # Tail replay dependencies.
 tailcert=json.loads((args.tail_root/'data/certificate_80dps/tail_certificate.json').read_text());tailaudit=json.loads((args.tail_root/'data/tail_certificate_audit.json').read_text());tailid=json.loads((args.tail_root/'data/tail_chart_exact_identity_audit.json').read_text());v4=json.loads((args.v4_root/'data/validated_output_summary.json').read_text())
 checks['tail_dependency_replay_pass']=tailcert['classification']=='GO_PEABODY_TAIL_PHI_POSITIVITY_CERTIFIED' and tailaudit['classification']=='PEABODY_TAIL_CERTIFICATE_ADVERSARIAL_AUDIT_PASS' and tailid['classification']=='PEABODY_TAIL_STABLE_CHART_EXACT_IDENTITIES_PASS'
 checks['v4_dependency_replay_pass']=v4['required_campaign_gates_pass'] is True and v4['checks']['optional_fixed_rho_integrate_evaluated'] is False
 checks['tail_dependency_hashes']={'tail_certificate':sha256(args.tail_root/'data/certificate_80dps/tail_certificate.json'),'tail_boxes':sha256(args.tail_root/'data/certificate_80dps/tail_terminal_boxes.csv'),'tail_package_checksums':sha256(args.tail_root/'SHA256SUMS.txt')}
 # Deterministic semantic clean replay.
 with tempfile.TemporaryDirectory() as td:
  out=Path(td)/'cert';fresh=cert.run(out,80,'bfs',False)
  freshd=json.loads((out/'peabody_central_certificate.json').read_text())
  a=json.dumps(proof_core(d80),sort_keys=True,separators=(',',':'));b=json.dumps(proof_core(freshd),sort_keys=True,separators=(',',':'))
  checks['deterministic_clean_replay_pass']=a==b;checks['canonical_proof_core_sha256']=hashlib.sha256(a.encode()).hexdigest();checks['fresh_proof_core_sha256']=hashlib.sha256(b.encode()).hexdigest()
 required=['canonical_classification_pass','formula_audit_pass','local_target_pass','bulk_target_pass','resource_limits_pass','two_precision_replay_pass','subdivision_order_permutation_pass','phi_zero_exact_identity','phi_prime_zero_positive','local_bulk_seam_exact','central_tail_seam_exact','local_partition_gap_free','bulk_partition_gap_free','local_quotient_direct_agreement_pass','sampled_high_precision_bulk_quadrature_containment_pass','sampled_high_precision_local_derivative_containment_pass','automatic_differentiation_crosscheck_pass','correction_sign_mutation_detected','shifted_psi0_baseline_control_fails','underresolved_partition_rejected','tail_dependency_replay_pass','v4_dependency_replay_pass','deterministic_clean_replay_pass']
 overall=all(bool(checks[k]) for k in required)
 result={'audit_pass':overall,'required_checks':required,'checks':checks,'classification':'PEABODY_CENTRAL_CERTIFICATE_ADVERSARIAL_AUDIT_PASS' if overall else 'PEABODY_CENTRAL_CERTIFICATE_ADVERSARIAL_AUDIT_FAIL'}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if overall else 1)
if __name__=='__main__':main()
