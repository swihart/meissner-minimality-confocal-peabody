#!/usr/bin/env python3
"""Outward-rounded central certificate for confocal Peabody Phi(e)>0.

The proof has two pieces:
  * local endpoint: certify Phi'(e) >= 1/2000 on 0 <= e <= 1/100;
    hence J(e)=Phi(e)/e >= 1/2000 with J(0)=Phi'(0).
  * compact bulk: certify Phi(e) > 1/10^7 on 1/100 <= e <= 199/200.

The authoritative fixed-interval formula is the validated stable q-chart,
q=(1-e)/(1+e).  x-integration uses a rigorous composite midpoint formula
with an interval second-derivative remainder.  Parameter slabs use a centered
mean-value form in q.  mpmath.iv is the outward-rounded proof authority.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, platform, sys, time
from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
from mpmath.libmp import to_str

FORMULA_VERSION="PEABODY_CENTRAL_STABLE_Q_V1"
CERTIFICATE_VERSION="PEABODY_CENTRAL_INTERVAL_V1"
DEFAULT_DPS=80
LOCAL_E0=Fraction(1,100)
CENTRAL_EMAX=Fraction(199,200)
LOCAL_Q_SLABS=16
X_PANELS=10
INITIAL_BULK_SEGMENTS=8
MAX_DEPTH=24
MAX_CENTRAL_BOXES=10000
MAX_NEW_DATA_BYTES=25_000_000
LOCAL_TARGET=Fraction(1,2000)
BULK_TARGET=Fraction(1,10_000_000)


def fracstr(f:Fraction)->str:return f"{f.numerator}/{f.denominator}"
def q_from_e(e:Fraction)->Fraction:return (1-e)/(1+e)
def e_from_q(q:Fraction)->Fraction:return (1-q)/(1+q)
def lcm(a:int,b:int)->int:return abs(a*b)//math.gcd(a,b)

def sha256(path:Path)->str:
 h=hashlib.sha256()
 with path.open('rb') as f:
  for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 return h.hexdigest()

@dataclass(frozen=True)
class C:
 iv:Any;one:Any;sqrt2:Any;kappa:Any;K:Any;psi0:Any;phi_prime0:Any


def setup(dps:int)->C:
 if dps<50:raise ValueError('precision must be at least 50 decimal digits')
 mp.iv.dps=dps;iv=mp.iv;one=iv.mpf(1);s2=iv.sqrt(2);kap=one+s2;K=kap*kap
 alpha=iv.atan2(2*s2,one)
 psi0=-(2*iv.pi/iv.sqrt(3))*alpha
 phi_prime0=(iv.mpf(1)/2)*(5*iv.pi/(3*iv.sqrt(3))-3+alpha*(3*s2/2-5*iv.sqrt(6)*iv.pi/18))
 return C(iv,one,s2,kap,K,psi0,phi_prime0)


def ivpoint(f:Fraction,c:C):return c.iv.mpf(f.numerator)/f.denominator
def ivhull(a:Fraction,b:Fraction,c:C):
 if a>b:a,b=b,a
 d=lcm(a.denominator,b.denominator)
 return c.iv.mpf([a.numerator*(d//a.denominator),b.numerator*(d//b.denominator)])/d

def endpoint(v:Any,which:str,digits:int)->str:
 t=v._mpi_[0 if which=='lower' else 1]
 return to_str(t,digits,strip_zeros=False)
def rec(v:Any,digits:int)->dict[str,str]:return {'lower':endpoint(v,'lower',digits),'upper':endpoint(v,'upper',digits)}

@dataclass
class D:
 v:Any;q:Any
 def __add__(self,o):o=asD(o);return D(self.v+o.v,self.q+o.q)
 __radd__=__add__
 def __sub__(self,o):o=asD(o);return D(self.v-o.v,self.q-o.q)
 def __rsub__(self,o):o=asD(o);return D(o.v-self.v,o.q-self.q)
 def __mul__(self,o):o=asD(o);return D(self.v*o.v,self.q*o.v+self.v*o.q)
 __rmul__=__mul__
 def __neg__(self):return D(-self.v,-self.q)
 def inv(self):return D(1/self.v,-self.q/(self.v*self.v))
 def __truediv__(self,o):return self*asD(o).inv()
 def __rtruediv__(self,o):return asD(o)*self.inv()
 def __pow__(self,n:int):
  if n==0:return asD(1)
  if n<0:return (self**(-n)).inv()
  out=asD(1);base=self
  while n:
   if n&1:out=out*base
   base=base*base;n//=2
  return out

@dataclass
class J:
 v:Any;x:Any;xx:Any
 def __add__(self,o):o=asJ(o);return J(self.v+o.v,self.x+o.x,self.xx+o.xx)
 __radd__=__add__
 def __sub__(self,o):o=asJ(o);return J(self.v-o.v,self.x-o.x,self.xx-o.xx)
 def __rsub__(self,o):o=asJ(o);return J(o.v-self.v,o.x-self.x,o.xx-self.xx)
 def __mul__(self,o):o=asJ(o);return J(self.v*o.v,self.x*o.v+self.v*o.x,self.xx*o.v+2*self.x*o.x+self.v*o.xx)
 __rmul__=__mul__
 def __neg__(self):return J(-self.v,-self.x,-self.xx)
 def inv(self):
  v=self.v;return J(1/v,-self.x/(v*v),2*self.x*self.x/(v*v*v)-self.xx/(v*v))
 def __truediv__(self,o):return self*asJ(o).inv()
 def __rtruediv__(self,o):return asJ(o)*self.inv()
 def __pow__(self,n:int):
  if n==0:return asJ(1)
  if n<0:return (self**(-n)).inv()
  out=asJ(1);base=self
  while n:
   if n&1:out=out*base
   base=base*base;n//=2
  return out

_IV=None
def asD(x):
 if isinstance(x,D):return x
 if hasattr(x,'_mpi_'):return D(x,_IV.mpf(0))
 return D(_IV.mpf(x),_IV.mpf(0))
def asJ(x):
 if isinstance(x,J):return x
 if isinstance(x,D):return J(x,asD(0),asD(0))
 return J(asD(x),asD(0),asD(0))
def sqrtD(x):x=asD(x);s=_IV.sqrt(x.v);return D(s,x.q/(2*s))
def atanD(x):x=asD(x);den=1+x.v*x.v;return D(_IV.atan2(x.v,_IV.mpf(1)),x.q/den)
def sqrtJ(x):
 x=asJ(x);s=sqrtD(x.v);return J(s,x.x/(2*s),x.xx/(2*s)-x.x*x.x/(4*s*s*s))
def atanJ(x):
 x=asJ(x);den=1+x.v*x.v
 return J(atanD(x.v),x.x/den,x.xx/den-2*x.v*x.x*x.x/(den*den))


def hjet(qv:Any,xv:Any,c:C,qder:bool=True,xder:bool=True,correction_sign:int=1)->J:
 global _IV;_IV=c.iv
 Q=J(D(qv,c.iv.mpf(1) if qder else c.iv.mpf(0)),asD(0),asD(0))
 X=J(D(xv,c.iv.mpf(0)),asD(1 if xder else 0),asD(0))
 one=asJ(1);K=asJ(c.K);s2=asJ(c.sqrt2);kap=asJ(c.kappa)
 DD=sqrtJ(K*K+Q*Q)
 R=sqrtJ(K*K+Q*Q-2*K*Q*X*X)
 T=sqrtJ(2*K*(K*K+Q*Q)+K*K*(one-Q)*(one-Q)*X*X)
 delta=2*K*(one-X*X)/(R+K-Q)
 Mq=K*(Q-2*K*X*X)/(R+K)+(one-K)*R-K*K-Q*R-Q-Q*Q
 primary=-16*s2*kap*(K*K+Q*Q)/(R*T)
 correction=-4*K*(one-Q*Q)*(K*K+Q*Q)*delta*Mq/(R*T*T*T)
 alg=-4*K*(one-Q*Q)*(K*K+Q*Q)*delta/(R*T*T)
 Z=K*((one+Q)*DD+(one-Q)*R)/(T*(K+Q+DD))
 return (primary+correction_sign*correction)*atanJ(Z)+alg


def domain_diagnostics(qlo:Fraction,qhi:Fraction,c:C)->dict[str,Any]:
 Q=ivhull(qlo,qhi,c);X=c.iv.mpf([0,1]);K=c.K;one=c.one
 D2=K*K+Q*Q;R2=K*K+Q*Q-2*K*Q*X*X;T2=2*K*(K*K+Q*Q)+K*K*(one-Q)*(one-Q)*X*X
 D=c.iv.sqrt(D2);R=c.iv.sqrt(R2);T=c.iv.sqrt(T2)
 vals={'D2':D2,'R2':R2,'T2':T2,'delta_den':R+K-Q,'R_plus_K':R+K,'angle_den':T*(K+Q+D),'angle_num':K*((one+Q)*D+(one-Q)*R)}
 vals['Z']=vals['angle_num']/vals['angle_den']
 return vals


def integrate_point(q:Fraction,c:C,xpan:int,records:bool=False)->tuple[Any,list[dict[str,Any]]]:
 h=c.iv.mpf(1)/xpan;total=c.iv.mpf(0);qv=ivpoint(q,c);rows=[]
 for i in range(xpan):
  m=c.iv.mpf(2*i+1)/(2*xpan);box=c.iv.mpf([i,i+1])/xpan
  hm=hjet(qv,m,c,qder=False);hb=hjet(qv,box,c,qder=False)
  midpoint=h*hm.v.v;remainder=(h*h*h/24)*hb.xx.v;contrib=midpoint+remainder;total+=contrib
  if records:rows.append({'x_panel_index':i,'h_mid':hm.v.v,'h_xx':hb.xx.v,'midpoint_contribution':midpoint,'remainder_contribution':remainder,'point_integral_contribution':contrib})
 return total,rows


def integrate_qder(qlo:Fraction,qhi:Fraction,c:C,xpan:int,records:bool=False)->tuple[Any,list[dict[str,Any]]]:
 h=c.iv.mpf(1)/xpan;total=c.iv.mpf(0);qv=ivhull(qlo,qhi,c);rows=[]
 for i in range(xpan):
  m=c.iv.mpf(2*i+1)/(2*xpan);box=c.iv.mpf([i,i+1])/xpan
  hm=hjet(qv,m,c,qder=True);hb=hjet(qv,box,c,qder=True)
  midpoint=h*hm.v.q;remainder=(h*h*h/24)*hb.xx.q;contrib=midpoint+remainder;total+=contrib
  if records:rows.append({'x_panel_index':i,'hq_mid':hm.v.q,'hq_xx':hb.xx.q,'midpoint_derivative_contribution':midpoint,'remainder_derivative_contribution':remainder,'q_derivative_integral_contribution':contrib})
 return total,rows


def local_certificate(c:C,xpan:int=X_PANELS,qslabs:int=LOCAL_Q_SLABS,records:bool=True)->tuple[dict[str,Any],list[dict[str,Any]]]:
 qmin=q_from_e(LOCAL_E0);width=(Fraction(1)-qmin)/qslabs;target=ivpoint(LOCAL_TARGET,c);digits=mp.iv.dps+20
 slabs=[];boxrows=[];worst=None
 for j in range(qslabs):
  qa=qmin+j*width;qb=qmin+(j+1)*width
  dpsi,rows=integrate_qder(qa,qb,c,xpan,records)
  Q=ivhull(qa,qb,c);dqde=-(1+Q)*(1+Q)/2;phie=dpsi*dqde/8
  ea=e_from_q(qb);eb=e_from_q(qa)
  slabs.append({'index':j,'e_lo':fracstr(ea),'e_hi':fracstr(eb),'q_lo':fracstr(qa),'q_hi':fracstr(qb),'dpsi_dq':rec(dpsi,digits),'phi_prime':rec(phie,digits),'exceeds_target':bool(phie.a>target.b)})
  if worst is None or bool(phie.a<worst):worst=phie.a
  if records:
   for r in rows:
    rr={'local_q_slab_index':j,'e_lo':fracstr(ea),'e_hi':fracstr(eb),'q_lo':fracstr(qa),'q_hi':fracstr(qb),'x_panel_index':r['x_panel_index'],'x_lo':f"{r['x_panel_index']}/{xpan}",'x_hi':f"{r['x_panel_index']+1}/{xpan}"}
    for k,v in r.items():
     if k!='x_panel_index':rr[k+'_lower']=endpoint(v,'lower',digits);rr[k+'_upper']=endpoint(v,'upper',digits)
    boxrows.append(rr)
 phi_e0=ivpoint(LOCAL_E0,c)*target
 summary={'method':'integrated derivative in stable q chart with composite midpoint interval quadrature','e_range':f"0 <= e <= {fracstr(LOCAL_E0)}",'q_range':f"{fracstr(qmin)} <= q <= 1",'q_slabs':qslabs,'x_panels':xpan,'terminal_boxes':qslabs*xpan,'exact_phi_prime_zero':'1/2*(5*pi/(3*sqrt(3))-3+acos(1/3)*(3*sqrt(2)/2-5*sqrt(6)*pi/18))','phi_prime_zero_enclosure':rec(c.phi_prime0,digits),'target_phi_prime':fracstr(LOCAL_TARGET),'worst_phi_prime_lower':endpoint(worst,'lower',digits),'all_slabs_exceed_target':all(s['exceeds_target'] for s in slabs),'conclusion':f"J(e)=Phi(e)/e >= {fracstr(LOCAL_TARGET)} on [0,{fracstr(LOCAL_E0)}], with J(0)=Phi'(0)",'phi_at_e0_simple_lower':fracstr(LOCAL_E0*LOCAL_TARGET),'slabs':slabs}
 return summary,boxrows


def bulk_slab(ea:Fraction,eb:Fraction,c:C,xpan:int,records:bool=False)->tuple[Any,dict[str,Any],list[dict[str,Any]]]:
 qlo=q_from_e(eb);qhi=q_from_e(ea);qm=(qlo+qhi)/2
 psi_mid,pr=integrate_point(qm,c,xpan,records);dpsi,dr=integrate_qder(qlo,qhi,c,xpan,records)
 dq=ivhull(qlo-qm,qhi-qm,c);psi=psi_mid+dq*dpsi;phi=(psi-c.psi0)/8
 info={'e_lo':fracstr(ea),'e_hi':fracstr(eb),'q_lo':fracstr(qlo),'q_hi':fracstr(qhi),'q_mid':fracstr(qm),'psi_mid':psi_mid,'dpsi_dq':dpsi,'psi_enclosure':psi,'phi_enclosure':phi}
 rows=[]
 if records:
  for p,d in zip(pr,dr):
   i=p['x_panel_index'];rr={'e_lo':fracstr(ea),'e_hi':fracstr(eb),'q_lo':fracstr(qlo),'q_hi':fracstr(qhi),'q_mid':fracstr(qm),'x_panel_index':i,'x_lo':f"{i}/{xpan}",'x_hi':f"{i+1}/{xpan}"}
   for src in (p,d):
    for k,v in src.items():
     if k!='x_panel_index':rr[k+'_lower']=v;rr[k+'_upper']=v
   rows.append(rr)
 return phi,info,rows


def adaptive_bulk(c:C,xpan:int=X_PANELS,order:str='bfs',target:Fraction=BULK_TARGET,records:bool=True)->tuple[dict[str,Any],list[dict[str,Any]],list[dict[str,Any]]]:
 initial=[];span=CENTRAL_EMAX-LOCAL_E0
 for j in range(INITIAL_BULK_SEGMENTS):initial.append((LOCAL_E0+span*j/INITIAL_BULK_SEGMENTS,LOCAL_E0+span*(j+1)/INITIAL_BULK_SEGMENTS,0))
 q=deque(initial);accepted=[];targetiv=ivpoint(target,c);max_slabs=MAX_CENTRAL_BOXES//xpan;start=time.time()
 while q:
  ea,eb,depth=(q.popleft() if order=='bfs' else q.pop())
  phi,info,_=bulk_slab(ea,eb,c,xpan,False)
  if bool(phi.a>targetiv.b):accepted.append((ea,eb,depth,phi,info))
  else:
   if depth>=MAX_DEPTH or len(accepted)+len(q)+2>max_slabs:raise RuntimeError(f'central bulk hard stop on {ea}..{eb}, depth {depth}, lower {phi}')
   m=(ea+eb)/2
   children=[(ea,m,depth+1),(m,eb,depth+1)]
   if order=='bfs':q.extend(children)
   elif order=='dfs':q.extend(children)
   elif order=='reverse':q.extend(reversed(children))
   else:raise ValueError(order)
 accepted.sort(key=lambda z:z[0]);digits=mp.iv.dps+20;boxrows=[];slabs=[];worst=None;maxdepth=0
 for idx,(ea,eb,depth,_,_) in enumerate(accepted):
  phi,info,rows=bulk_slab(ea,eb,c,xpan,records);maxdepth=max(maxdepth,depth)
  if worst is None or bool(phi.a<worst):worst=phi.a
  slabs.append({'index':idx,'depth':depth,'e_lo':fracstr(ea),'e_hi':fracstr(eb),'q_lo':info['q_lo'],'q_hi':info['q_hi'],'q_mid':info['q_mid'],'psi_mid':rec(info['psi_mid'],digits),'dpsi_dq':rec(info['dpsi_dq'],digits),'psi_enclosure':rec(info['psi_enclosure'],digits),'phi_enclosure':rec(phi,digits),'exceeds_target':bool(phi.a>targetiv.b)})
  if records:
   for r in rows:
    rr={'bulk_slab_index':idx,'depth':depth,**{k:v for k,v in r.items() if not k.endswith('_lower') and not k.endswith('_upper')}}
    for k,v in r.items():
     if k.endswith('_lower') or k.endswith('_upper'):
      base=k.rsplit('_',1)[0];which=k.rsplit('_',1)[1];rr[k]=endpoint(v,which,digits)
    boxrows.append(rr)
 summary={'method':'centered q mean-value form plus composite midpoint interval quadrature','e_range':f"{fracstr(LOCAL_E0)} <= e <= {fracstr(CENTRAL_EMAX)}",'q_range':f"{fracstr(q_from_e(CENTRAL_EMAX))} <= q <= {fracstr(q_from_e(LOCAL_E0))}",'initial_segments':INITIAL_BULK_SEGMENTS,'accepted_slabs':len(slabs),'x_panels':xpan,'terminal_boxes':len(slabs)*xpan,'maximum_depth':maxdepth,'subdivision_order':order,'simple_rational_target':fracstr(target),'worst_phi_lower':endpoint(worst,'lower',digits),'all_slabs_exceed_target':all(s['exceeds_target'] for s in slabs),'elapsed_seconds':time.time()-start,'slabs':slabs}
 return summary,boxrows,slabs


def write_csv(path:Path,rows:list[dict[str,Any]])->None:
 if not rows:return
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0].keys()),extrasaction='ignore');w.writeheader();w.writerows(rows)


def run(output:Path,dps:int,order:str='bfs',write_boxes:bool=True)->dict[str,Any]:
 start=time.time();output.mkdir(parents=True,exist_ok=True);c=setup(dps);digits=dps+20
 global_diag=domain_diagnostics(q_from_e(CENTRAL_EMAX),Fraction(1),c)
 domain={k:{**rec(v,digits),'strictly_positive':bool(v.a>0)} for k,v in global_diag.items()}
 local,localrows=local_certificate(c,records=write_boxes)
 bulk,bulkrows,_=adaptive_bulk(c,order=order,records=write_boxes)
 total_boxes=local['terminal_boxes']+bulk['terminal_boxes']
 if total_boxes>MAX_CENTRAL_BOXES:raise RuntimeError('central terminal-box hard stop exceeded')
 if write_boxes:
  write_csv(output/'central_local_terminal_boxes.csv',localrows);write_csv(output/'central_bulk_terminal_boxes.csv',bulkrows)
  write_csv(output/'central_local_slab_summary.csv',[{k:v for k,v in s.items() if k!='phi_prime' and k!='dpsi_dq'}|{'phi_prime_lower':s['phi_prime']['lower'],'phi_prime_upper':s['phi_prime']['upper']} for s in local['slabs']])
  write_csv(output/'central_bulk_slab_summary.csv',[{'index':s['index'],'depth':s['depth'],'e_lo':s['e_lo'],'e_hi':s['e_hi'],'q_lo':s['q_lo'],'q_hi':s['q_hi'],'q_mid':s['q_mid'],'phi_lower':s['phi_enclosure']['lower'],'phi_upper':s['phi_enclosure']['upper'],'exceeds_target':s['exceeds_target']} for s in bulk['slabs']])
 passed=local['all_slabs_exceed_target'] and bulk['all_slabs_exceed_target'] and all(v['strictly_positive'] for v in domain.values())
 summary={'certificate_version':CERTIFICATE_VERSION,'formula_version':FORMULA_VERSION,'interval_precision_decimal_digits':dps,'python_version':sys.version,'platform':platform.platform(),'mpmath_version':mp.__version__,'proof_authority':'mpmath.iv outward-rounded interval arithmetic','local_endpoint':local,'bulk':bulk,'global_domain_diagnostics':domain,'new_central_terminal_boxes':total_boxes,'maximum_new_central_boxes':MAX_CENTRAL_BOXES,'maximum_adaptive_depth':MAX_DEPTH,'elapsed_seconds':time.time()-start,'proof_status':'CERTIFIED' if passed else 'NOT_CERTIFIED','classification':'GO_PEABODY_CENTRAL_PHI_POSITIVITY_CERTIFIED' if passed else 'NO_GO_PEABODY_CENTRAL_INTERVAL'}
 path=output/'peabody_central_certificate.json';path.write_text(json.dumps(summary,indent=2)+'\n')
 files=[p for p in output.iterdir() if p.is_file()];size=sum(p.stat().st_size for p in files);summary['new_certificate_data_bytes']=size;summary['certificate_size_pass']=size<=MAX_NEW_DATA_BYTES;summary['hard_stop_pass']=total_boxes<=MAX_CENTRAL_BOXES and bulk['maximum_depth']<=MAX_DEPTH and summary['certificate_size_pass'];path.write_text(json.dumps(summary,indent=2)+'\n')
 (output/'central_certificate_file_hashes.json').write_text(json.dumps({p.name:sha256(p) for p in output.iterdir() if p.is_file() and p.name!='central_certificate_file_hashes.json'},indent=2)+'\n')
 print(json.dumps(summary,indent=2));return summary


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--precision-dps',type=int,default=DEFAULT_DPS);ap.add_argument('--order',choices=['bfs','dfs','reverse'],default='bfs');ap.add_argument('--no-boxes',action='store_true');args=ap.parse_args()
 s=run(args.output_dir,args.precision_dps,args.order,not args.no_boxes);raise SystemExit(0 if s['proof_status']=='CERTIFIED' else 1)
if __name__=='__main__':main()
