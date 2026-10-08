#!/usr/bin/env python3
"""High-precision cross-check and freeze of the central Peabody q-chart."""
from __future__ import annotations
import csv, hashlib, json, platform, sys, time
from fractions import Fraction
from pathlib import Path
import mpmath as mp

FORMULA_VERSION = "PEABODY_CENTRAL_STABLE_Q_V1"
WORKING_DPS = 110
ROOT = Path(__file__).resolve().parents[1]

mp.mp.dps = WORKING_DPS
S2 = mp.sqrt(2); KAPPA = 1 + S2; K = KAPPA*KAPPA
ALPHA = mp.atan2(2*S2, 1)
PSI0 = -(2*mp.pi/mp.sqrt(3))*ALPHA


def sha256(path: Path) -> str:
    h=hashlib.sha256();
    with path.open('rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()


def original_h(e: mp.mpf, x: mp.mpf) -> mp.mpf:
    b2=(3+4*S2*e+3*e*e)/(1-e*e)
    b=mp.sqrt(b2); a=b/mp.sqrt(1-e*e)
    amp=mp.sqrt(1-x*x/b2); c=e*amp
    u=mp.sqrt(1-1/b2); v=mp.sqrt(1+1/b2)
    y=1/(mp.sqrt(b2+1)+b)
    angle=mp.atan(y*mp.sqrt((1+c)/(1-c)))
    kernel=4*angle/mp.sqrt(1-c*c)
    core=kernel/a+e*(amp-u)/(1-c*c)*((v*c-1)*kernel+2/b)
    return -4*b*core/amp


def stable_q_h(q: mp.mpf, x: mp.mpf, correction_sign: int = 1) -> mp.mpf:
    D=mp.sqrt(K*K+q*q)
    R=mp.sqrt(K*K+q*q-2*K*q*x*x)
    T=mp.sqrt(2*K*(K*K+q*q)+K*K*(1-q)*(1-q)*x*x)
    delta=2*K*(1-x*x)/(R+K-q)
    Mq=K*(q-2*K*x*x)/(R+K)+(1-K)*R-K*K-q*R-q-q*q
    primary=-16*S2*KAPPA*(K*K+q*q)/(R*T)
    correction=-4*K*(1-q*q)*(K*K+q*q)*delta*Mq/(R*T**3)
    alg=-4*K*(1-q*q)*(K*K+q*q)*delta/(R*T*T)
    Z=K*((1+q)*D+(1-q)*R)/(T*(K+q+D))
    return (primary+correction_sign*correction)*mp.atan(Z)+alg


def q_from_e(e: mp.mpf) -> mp.mpf:
    return (1-e)/(1+e)


def mandated_values() -> list[Fraction]:
    vals=[Fraction(0), Fraction(1,10**8), Fraction(1,10**6), Fraction(1,10**4),
          Fraction(1,1000), Fraction(1,100), Fraction(1,10), Fraction(1,2),
          Fraction(9,10), Fraction(99,100), Fraction(199,200)]
    vals += [Fraction(k,32) for k in list(range(1,16))+list(range(17,32))]
    # preserve order and uniqueness
    out=[]
    for v in vals:
        if v not in out: out.append(v)
    assert len(out)>=41
    return out


def main() -> None:
    start=time.time(); outdir=ROOT/'data'; outdir.mkdir(parents=True,exist_ok=True)
    vals=mandated_values(); xvals=[Fraction(0),Fraction(1,7),Fraction(1,3),Fraction(1,2),Fraction(2,3),Fraction(6,7),Fraction(1)]
    rows=[]; max_h=mp.mpf(0); max_psi=mp.mpf(0); max_phi=mp.mpf(0)
    integral_rows=[]
    for ef in vals:
        e=mp.mpf(ef.numerator)/ef.denominator; q=q_from_e(e)
        for xf in xvals:
            x=mp.mpf(xf.numerator)/xf.denominator
            ho=original_h(e,x); hs=stable_q_h(q,x); err=abs(ho-hs); max_h=max(max_h,err)
            rows.append({'e':str(ef),'q':mp.nstr(q,50),'x':str(xf),'h_original':mp.nstr(ho,90),'h_stable_q':mp.nstr(hs,90),'abs_difference':mp.nstr(err,25)})
        po=mp.quad(lambda xx: original_h(e,xx),[0,1])
        ps=mp.quad(lambda xx: stable_q_h(q,xx),[0,1])
        er=abs(po-ps); max_psi=max(max_psi,er)
        phio=(po-PSI0)/8; phis=(ps-PSI0)/8; ep=abs(phio-phis);max_phi=max(max_phi,ep)
        integral_rows.append({'e':str(ef),'q':mp.nstr(q,60),'psi_original':mp.nstr(po,100),'psi_stable_q':mp.nstr(ps,100),'phi_original':mp.nstr(phio,100),'phi_stable_q':mp.nstr(phis,100),'abs_psi_difference':mp.nstr(er,30),'abs_phi_difference':mp.nstr(ep,30)})
    with (outdir/'central_original_vs_stable_pointwise.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    with (outdir/'central_original_vs_stable_integrals.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=integral_rows[0].keys());w.writeheader();w.writerows(integral_rows)
    # Exact endpoint identities.
    phi0=(mp.quad(lambda xx: stable_q_h(mp.mpf(1),xx),[0,1])-PSI0)/8
    summary={
      'formula_version':FORMULA_VERSION,'chart':'q=(1-e)/(1+e)','working_precision_decimal_digits':WORKING_DPS,
      'parameter_values':len(vals),'mandated_values_included':True,'additional_rational_or_dyadic_values':len(vals)-11,
      'x_values_per_parameter':len(xvals),'pointwise_cases':len(rows),
      'maximum_pointwise_integrand_difference':mp.nstr(max_h,40),
      'maximum_integral_psi_difference':mp.nstr(max_psi,40),
      'maximum_integral_phi_difference':mp.nstr(max_phi,40),
      'phi_zero_numeric_residual':mp.nstr(phi0,40),
      'psi0_exact':'-(2*pi/sqrt(3))*acos(1/3)',
      'pass':bool(max_h<mp.mpf('1e-95') and max_psi<mp.mpf('1e-95') and abs(phi0)<mp.mpf('1e-95')),
      'python_version':sys.version,'platform':platform.platform(),'mpmath_version':mp.__version__,'elapsed_seconds':time.time()-start,
    }
    summary['classification']='PEABODY_CENTRAL_FORMULA_FROZEN' if summary['pass'] else 'PEABODY_CENTRAL_FORMULA_AUDIT_FAIL'
    (outdir/'central_formula_audit.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    raise SystemExit(0 if summary['pass'] else 1)

if __name__=='__main__': main()
