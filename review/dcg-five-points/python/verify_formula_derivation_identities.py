#!/usr/bin/env python3
"""Exact algebraic checks for the Peabody formula derivation supplement."""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp


def poly_remainder_zero(expr, variable, relation):
    num = sp.together(expr).as_numer_denom()[0]
    p = sp.Poly(sp.expand(num), variable)
    r = sp.Poly(sp.expand(relation), variable)
    rem = p.rem(r).as_expr()
    return sp.factor(rem)


def main(output: Path):
    e,q,x,K,R,D,T = sp.symbols('e q x K R D T', real=True)
    rt2 = sp.sqrt(2)
    B = (3+3*e**2+4*rt2*e)/(1-e**2)
    width_plus = sp.factor((B+1) - 2*(e+rt2)**2/(1-e**2))
    width_minus = sp.factor((B-1) - 2*(rt2*e+1)**2/(1-e**2))

    Rrel = R**2-(K**2+q**2-2*K*q*x**2)
    Drel = D**2-(K**2+q**2)
    Trel = T**2-(2*K*(K**2+q**2)+K**2*(1-q)**2*x**2)

    delta_unstable=(R-K+q)/q
    delta_stable=2*K*(1-x**2)/(R+K-q)
    delta_rem=poly_remainder_zero(delta_unstable-delta_stable,R,Rrel)

    Bnum=(1-q)*(K+q)*R-(1+q)*(K**2+q**2)
    M_unstable=Bnum/q
    M_stable=K*(q-2*K*x**2)/(R+K)+(1-K)*R-K**2-q*R-q-q**2
    M_rem=poly_remainder_zero(M_unstable-M_stable,R,Rrel)

    Aplus=(1+q)*D+(1-q)*R
    Aminus=(1+q)*D-(1-q)*R
    product=Aplus*Aminus
    product_expr=sp.expand(product - (2*q/K)*T**2)
    # Reduce successively using R^2, D^2, T^2.
    num=sp.together(product_expr).as_numer_denom()[0]
    num=sp.Poly(sp.expand(num),T).rem(sp.Poly(sp.expand(Trel),T)).as_expr()
    num=sp.Poly(sp.expand(num),D).rem(sp.Poly(sp.expand(Drel),D)).as_expr()
    num=sp.Poly(sp.expand(num),R).rem(sp.Poly(sp.expand(Rrel),R)).as_expr()
    product_rem=sp.factor(num)

    z_original_sq=(2*K*q/(K+q+D)**2)*(Aplus/Aminus)
    z_stable_sq=K**2*Aplus**2/(T**2*(K+q+D)**2)
    # Cross-multiplied difference.  Factor off the positive Aplus term;
    # the remaining factor is exactly the angle-product identity.
    z_inner=sp.expand(2*q*T**2-K*Aplus*Aminus)
    num=sp.together(z_inner).as_numer_denom()[0]
    num=sp.Poly(sp.expand(num),T).rem(sp.Poly(sp.expand(Trel),T)).as_expr()
    num=sp.Poly(sp.expand(num),D).rem(sp.Poly(sp.expand(Drel),D)).as_expr()
    num=sp.Poly(sp.expand(num),R).rem(sp.Poly(sp.expand(Rrel),R)).as_expr()
    z_cross=sp.factor(num)

    # Scaling table from shifted rapidity rho^2=K/q.
    rho2=K/q
    d2=(K**2+q**2)/q**2
    rscale=R/q
    tscale=T/q
    am=K*(1-q)/q
    ap=K*(1+q)/q
    delta_rho=delta_stable
    m_rho=K*Bnum/q**3
    p2_rho=sp.factor(-4*am*ap*d2*delta_rho*m_rho/(rho2**2*rscale*tscale**3))
    p2_stable=sp.factor(-4*K*(1-q**2)*(K**2+q**2)*delta_stable*M_stable/(R*T**3))
    p2_rem=poly_remainder_zero(p2_rho-p2_stable,R,Rrel)
    q0_rho=sp.factor(-4*am*ap*d2*delta_rho/(rho2*rscale*tscale**2))
    q0_stable=sp.factor(-4*K*(1-q**2)*(K**2+q**2)*delta_stable/(R*T**2))
    q0_rem=sp.factor(q0_rho-q0_stable)

    checks={
      'beam_width_B_plus_one_identity': str(width_plus),
      'beam_width_B_minus_one_identity': str(width_minus),
      'delta_rationalization_remainder': str(delta_rem),
      'M_rationalization_remainder': str(M_rem),
      'angle_product_identity_remainder': str(product_rem),
      'angle_argument_squared_cross_difference': str(z_cross),
      'P2_scaling_remainder': str(p2_rem),
      'Q0_scaling_remainder': str(q0_rem),
    }
    passed=all(v=='0' for v in checks.values())
    result={'classification':'PEABODY_FORMULA_DERIVATION_IDENTITIES_PASS' if passed else 'PEABODY_FORMULA_DERIVATION_IDENTITIES_FAIL','pass':passed,'checks':checks}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if passed else 1)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.output)
