#!/usr/bin/env python3
"""Format archived diagnostic endpoints with outward decimal rounding.

This does not generate an Arb certificate. Printed lower endpoints are rounded
down and upper endpoints up relative to the archived decimal display. The
canonical publication gates remain checks of the original exact binary bounds.
"""
import argparse
import json
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING, localcontext
from pathlib import Path


def directed(value, lower):
    value = Decimal(value)
    with localcontext() as ctx:
        ctx.prec = max(220, len(value.as_tuple().digits) + 10)
        quantum = Decimal(1).scaleb(value.adjusted() - 12)
        shown = value.quantize(quantum, rounding=ROUND_FLOOR if lower else ROUND_CEILING)
    assert shown <= value if lower else shown >= value
    coefficient, exponent = format(shown, '.12E').split('E')
    return '$' + coefficient + r'\times 10^{' + str(int(exponent)) + '}$'


def write_table(path, report):
    history = report['archived_endpoint_interval_implementations']
    runs = report['arb']['runs']
    endpoints = report['arb']['endpoint_runs']
    rows = [
        (r'legacy \texttt{mpmath.iv}', '32/10/4', history['legacy_mpmath_iv']['endpoint_lower'], history['legacy_mpmath_iv']['worst_phi_second_upper']),
        ('direct MPFR', '32/10/4', history['direct_mpfr']['endpoint_lower'], history['direct_mpfr']['worst_phi_second_upper']),
        ('Arb canonical', '32/10/4', endpoints[0]['lower'], runs[0]['worst_phi_second_upper']),
        ('Arb refined', '128/20/16', endpoints[-1]['lower'], runs[-1]['worst_phi_second_upper']),
    ]
    lines = [r'\begin{table}[tbp]', r'\centering', r'\footnotesize', r'\setlength{\tabcolsep}{4pt}',
             r'\begin{tabular}{llcc}', r'\toprule',
             r'implementation & $N_q/N_x/N_0$ & lower endpoint for $\Phi(1)$ & upper endpoint for $\Phi^{\prime\prime}$ \\',
             r'\midrule']
    for label, grid, low, high in rows:
        lines.append(f'{label} & {grid} & {directed(low, True)} & {directed(high, False)} ' + r'\\')
    lines += [r'\bottomrule', r'\end{tabular}',
              r'\caption{Archived enclosure comparison. $N_q$ is the number of parameter slabs, $N_x$ the integration panels per slab, and $N_0$ the endpoint panels. Lower displays are rounded downward and upper displays upward. Only the canonical Arb certificate supplies the published rational bounds; refined and endpoint-interval results document provenance.}',
              r'\label{tab:enclosure-reconciliation}', r'\end{table}', '']
    Path(path).write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    write_table(args.output, json.loads(args.report.read_text()))
