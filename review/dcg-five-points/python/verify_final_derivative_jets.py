#!/usr/bin/env python3
"""Exact finite audit of production derivative rules via independent Taylor series.

No interval or transcendental replay.  The atan constant is set to zero on both
sides: only its positive-order derivatives are compared.  All other components
are compared exactly over Fraction.  This supplements the analytic rule audit.
"""
import ast
import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from typing import Any

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo-root',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args = parser.parse_args()
SOURCE = args.repo_root / 'review/dcg-five-points/arb/peabody_arb_concavity.py'
OUT = args.output


class ExactScalar:
    def __init__(self, value=0):
        self.v = value.v if isinstance(value, ExactScalar) else F(value)

    def __add__(self, other): return ExactScalar(self.v + ExactScalar(other).v)
    __radd__ = __add__
    def __neg__(self): return ExactScalar(-self.v)
    def __sub__(self, other): return self + (-ExactScalar(other))
    def __rsub__(self, other): return ExactScalar(other) - self
    def __mul__(self, other): return ExactScalar(self.v * ExactScalar(other).v)
    __rmul__ = __mul__
    def __truediv__(self, other): return ExactScalar(self.v / ExactScalar(other).v)
    def __rtruediv__(self, other): return ExactScalar(other) / self
    def __pow__(self, n): return ExactScalar(self.v ** n)
    def sqrt(self):
        a, b = math.isqrt(self.v.numerator), math.isqrt(self.v.denominator)
        assert F(a*a, b*b) == self.v
        return ExactScalar(F(a, b))
    def atan(self): return ExactScalar(0)


names = {'D3','X2','as_d3','as_x2','sqrt_d3','atan_d3','sqrt_x2','atan_x2'}
tree = ast.parse(SOURCE.read_text())
nodes = [n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names]
ns = {'dataclass':dataclass, 'arb':ExactScalar, 'Any':Any}
exec(compile(ast.Module(body=nodes, type_ignores=[]),str(SOURCE),'exec'),ns)
D3, X2 = ns['D3'], ns['X2']

# Independent truncated bivariate Taylor algebra: coefficients are divided
# derivatives, whereas the production jets store ordinary derivatives.
INDICES = [(i,j) for j in range(3) for i in range(4)]
def p(v):
    return v if isinstance(v,dict) else {(0,0):F(v)}
def add(a,b):
    a,b=p(a),p(b)
    return {k:a.get(k,F(0))+b.get(k,F(0)) for k in INDICES}
def scale(a,c): return {k:v*c for k,v in p(a).items()}
def mul(a,b):
    out={k:F(0) for k in INDICES}
    for (i,j),v in p(a).items():
        for (k,l),w in p(b).items():
            if i+k<=3 and j+l<=2: out[(i+k,j+l)] += v*w
    return out
def power(a,n):
    out=p(1)
    for _ in range(n):out=mul(out,a)
    return out
def series_compose(a,coefficients):
    a0=p(a).get((0,0),F(0))
    z=add(a,-a0)
    out=p(0)
    for n,c in enumerate(coefficients):out=add(out,scale(power(z,n),c))
    return out
def inv(a):
    a0=p(a)[(0,0)]
    return series_compose(a,[(-1)**n/a0**(n+1) for n in range(6)])
def sqroot(a):
    a0=p(a)[(0,0)]
    root=ExactScalar(a0).sqrt().v
    c=F(1); coefficients=[]
    for n in range(6):
        coefficients.append(root*c/a0**n)
        c*= (F(1,2)-n)/(n+1)
    return series_compose(a,coefficients)
def arctangent(a):
    # Coefficients of d/dz atan(a0+z)=1/(1+(a0+z)^2).
    a0=p(a)[(0,0)]; d=1+a0*a0
    derivative=[]
    for n in range(5):
        rhs=F(n==0)
        if n>=1:rhs-=2*a0*derivative[n-1]
        if n>=2:rhs-=derivative[n-2]
        derivative.append(rhs/d)
    return series_compose(a,[F(0)]+[v/(n+1) for n,v in enumerate(derivative)])
def to_jet(a):
    jets=[]
    for j in range(3):
        jets.append(D3(*(ExactScalar(a.get((i,j),0)*math.factorial(i)*math.factorial(j)) for i in range(4))))
    return X2(*jets)
def from_jet(a):
    out={}
    for j,field in enumerate(('v','x','xx')):
        qjet=getattr(a,field)
        for i,qfield in enumerate(('v','d1','d2','d3')):
            out[(i,j)]=getattr(qjet,qfield).v/F(math.factorial(i)*math.factorial(j))
    return out


checks={}
for seed in (1,2,3):
    a={k:F((-1)**(sum(k)+seed)*(1+seed+k[0]+3*k[1]),7+seed) for k in INDICES}
    b={k:F((-1)**(k[0]+seed)*(2+2*seed+2*k[0]+k[1]),5+seed) for k in INDICES}
    a[(0,0)]=F(4);b[(0,0)]=F(9)
    ja,jb=to_jet(a),to_jet(b)
    cases=[('add',ja+jb,add(a,b)),('subtract',ja-jb,add(a,scale(b,-1))),
           ('multiply',ja*jb,mul(a,b)),('reciprocal',ja.inv(),inv(a)),
           ('divide',ja/jb,mul(a,inv(b))),('sqrt',ns['sqrt_x2'](ja),sqroot(a)),
           ('atan',ns['atan_x2'](ja),arctangent(a)),('cube',ja**3,power(a,3))]
    for label,got,want in cases:
        got=from_jet(got)
        for k in INDICES:
            if label=='atan' and k==(0,0):continue
            checks[f'{seed}:{label}:q{k[0]}x{k[1]}']=got[k]==want.get(k,0)

mutation_text=SOURCE.read_text().replace('(6 * value.v**2 - 2)', '(6 * value.v**2 + 2)')
assert mutation_text != SOURCE.read_text()
mutation_tree=ast.parse(mutation_text)
mutation_nodes=[n for n in mutation_tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names]
mutns={'dataclass':dataclass,'arb':ExactScalar,'Any':Any}
exec(compile(ast.Module(body=mutation_nodes,type_ignores=[]),'<intentional atan sign mutation>','exec'),mutns)
mutjet=mutns['D3'](*(ExactScalar(a.get((i,0),0)*math.factorial(i)) for i in range(4)))
mutout=mutns['atan_d3'](mutjet)
mutation_rejected=mutout.d3.v/F(6) != arctangent(a)[(3,0)]
checks['negative_control:atan_third_derivative_sign_rejected']=mutation_rejected

result={'classification':'PEABODY_PRODUCTION_JET_EXACT_FINITE_AUDIT_PASS' if all(checks.values()) else 'FAIL',
        'pass':all(checks.values()),'checks_count':len(checks),'failures':[k for k,v in checks.items() if not v],
        'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'scope':'Three exact rational mixed-jet assignments checked against independent bivariate Taylor convolution; no fresh Arb replay and no new scalar bounds.',
        'excluded':'Arctangent zeroth-order transcendental values and rigorous interval enclosure semantics are not tested here.',
        'negative_controls':{'atan_third_derivative_sign_mutation_rejected':mutation_rejected},
        'checks':checks}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(result['classification'],result['checks_count'],result['failures'])
raise SystemExit(0 if result['pass'] else 2)
