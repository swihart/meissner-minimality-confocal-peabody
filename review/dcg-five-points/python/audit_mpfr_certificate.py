#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 160

def D(s: str) -> Decimal:
    return Decimal(s)

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''): h.update(chunk)
    return h.hexdigest()

def load(path: Path): return json.loads(path.read_text())

def overlap(a_lo,a_hi,b_lo,b_hi): return max(D(a_lo),D(b_lo)) <= min(D(a_hi),D(b_hi))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mpfr-forward',type=Path,required=True)
    ap.add_argument('--mpfr-512',type=Path,required=True)
    ap.add_argument('--mpfr-reverse',type=Path,required=True)
    ap.add_argument('--underresolved',type=Path,required=True)
    ap.add_argument('--mutation',type=Path,required=True)
    ap.add_argument('--mpmath',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    f=load(a.mpfr_forward); p512=load(a.mpfr_512); rev=load(a.mpfr_reverse)
    under=load(a.underresolved); mut=load(a.mutation); mp=load(a.mpmath)
    checks={}
    checks['forward_pass']=f['pass'] is True
    checks['precision_replay_pass']=p512['pass'] is True
    checks['reverse_replay_pass']=rev['pass'] is True
    checks['underresolved_rejected']=under['pass'] is False
    checks['mutation_rejected']=mut['pass'] is False
    checks['mpfr_version_recorded']=bool(f.get('mpfr_version'))
    checks['weaker_endpoint_headroom']=D(f['endpoint']['phi_one_lower']) > Decimal(1)/Decimal(4000)
    checks['weaker_concavity_headroom']=D(f['concavity']['worst_phi_second_upper']) < -Decimal(1)/Decimal(30000)
    checks['forward_512_same_endpoint']=f['endpoint']['phi_one_lower']==p512['endpoint']['phi_one_lower'] and f['endpoint']['phi_one_upper']==p512['endpoint']['phi_one_upper']
    checks['forward_reverse_same_endpoint']=f['endpoint']['phi_one_lower']==rev['endpoint']['phi_one_lower'] and f['endpoint']['phi_one_upper']==rev['endpoint']['phi_one_upper']
    checks['forward_512_same_worst']=f['concavity']['worst_phi_second_upper']==p512['concavity']['worst_phi_second_upper']
    checks['forward_reverse_same_worst']=f['concavity']['worst_phi_second_upper']==rev['concavity']['worst_phi_second_upper']
    checks['endpoint_overlap_mpmath']=overlap(f['endpoint']['phi_one_lower'],f['endpoint']['phi_one_upper'],mp['endpoint']['phi_one_enclosure']['lower'],mp['endpoint']['phi_one_enclosure']['upper'])
    mp_slabs={int(x['index']):x for x in mp['concavity']['slabs']}
    slab_overlap=[]
    with (a.mpfr_forward.parent/'concavity_slab_summary.csv').open(newline='',encoding='utf-8') as stream:
        for row in csv.DictReader(stream):
            m=mp_slabs[int(row['index'])]
            slab_overlap.append(overlap(row['phi_second_lower'],row['phi_second_upper'],m['phi_second']['lower'],m['phi_second']['upper']))
    checks['all_32_slab_intervals_overlap_mpmath']=all(slab_overlap) and len(slab_overlap)==32
    checks['all_domain_diagnostics_positive']=all(v['strictly_positive'] for v in f['domain_diagnostics'].values())
    result={
      'classification':'PEABODY_MPFR_CERTIFICATE_AUDIT_PASS' if all(checks.values()) else 'PEABODY_MPFR_CERTIFICATE_AUDIT_FAIL',
      'pass':all(checks.values()),
      'checks':checks,
      'forward_certificate_sha256':sha256(a.mpfr_forward),
      'mpmath_certificate_sha256':sha256(a.mpmath),
      'endpoint_lower':f['endpoint']['phi_one_lower'],
      'endpoint_target':'1/4000',
      'worst_phi_second_upper':f['concavity']['worst_phi_second_upper'],
      'concavity_target':'-1/30000',
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['pass'] else 1)
if __name__=='__main__': main()
