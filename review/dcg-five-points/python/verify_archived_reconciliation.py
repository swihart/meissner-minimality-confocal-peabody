#!/usr/bin/env python3
"""Independently audit archived Peabody reconciliation with stdlib arithmetic.

No Arb or MPFR evaluation is performed. Decimal strings are compared as
historical diagnostic displays, NOT treated as outward-directed exact bounds.
The publication gates are checked using exact dyadic endpoints. Concavity is
also reconstructed with Fractions from archived exact terminal contributions.
Those inputs remain trusted enclosures from the original Arb computation.
"""
import argparse
import csv
import hashlib
import json
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
from pathlib import Path

getcontext().prec = 220


def audit(root, output):
    root = root.resolve()
    checkpoint = root / 'review/dcg-five-points'
    recon = checkpoint / 'results/enclosure-reconciliation'
    arb = checkpoint / 'results/arb'
    mpfr = checkpoint / 'preflight/assistant_mpfr_runtime_only'
    inputs, checks = {}, {}

    def read(path):
        data = path.read_bytes()
        inputs[str(path.relative_to(root))] = hashlib.sha256(data).hexdigest()
        return data.decode('utf-8')

    def doc(path):
        return json.loads(read(path))

    def rows(path):
        return list(csv.DictReader(read(path).splitlines()))

    def ck(label, value):
        if label in checks:
            raise ValueError('duplicate check label: ' + label)
        checks[label] = bool(value)

    def boolean(text):
        if str(text).lower() not in ('true', 'false'):
            raise ValueError('not a Boolean: ' + str(text))
        return str(text).lower() == 'true'

    def pair(row, prefix=''):
        return D(row[prefix + 'lower']), D(row[prefix + 'upper'])

    def overlap(a, b):
        return max(a[0], b[0]) <= min(a[1], b[1])

    def contains(a, b):
        return a[0] <= b[0] <= b[1] <= a[1]

    def binary(point):
        return F(int(point['mantissa'])) * F(2) ** int(point['exponent'])

    def binary_pair(row, prefix):
        return tuple(binary({'mantissa': row[prefix + '_' + side + '_mantissa'],
                             'exponent': row[prefix + '_' + side + '_exponent']})
                     for side in ('lower', 'upper'))

    def add(a, b):
        return a[0] + b[0], a[1] + b[1]

    def multiply(a, b):
        products = [x * y for x in a for y in b]
        return min(products), max(products)

    def hashes(directory):
        manifest = doc(directory / 'OUTPUT_SHA256.json')
        return bool(manifest) and all(
            hashlib.sha256(read(directory / name).encode('utf-8')).hexdigest() == digest
            for name, digest in manifest.items())

    summary = doc(recon / 'enclosure_reconciliation.json')
    ck('archived reconciliation verdict and aggregate flags',
       summary['classification'] == 'PEABODY_ENCLOSURE_RECONCILIATION_PASS'
       and summary['pass'] is True
       and all(summary['arb'][key] is True for key in (
           'worst_upper_tightens_monotonically', 'all_runs_prove_strict_concavity',
           'all_runs_prove_minus_1_over_100000', 'all_endpoint_runs_prove_1_over_4000'))
       and summary['arb_mpfr_comparison']['all_aggregated_arb_intervals_intersect_mpfr'] is True)
    configurations = [(32, 10), (64, 20), (128, 20)]
    runs = rows(recon / 'arb_refinement_runs.csv')
    endpoints = rows(recon / 'endpoint_refinement_runs.csv')
    ck('exactly three runs and three endpoint runs', len(runs) == len(endpoints) == 3)
    slabs = {}
    for j, (n, m) in enumerate(configurations):
        ss = rows(recon / f'arb_slabs_{n}x{m}.csv')
        slabs[n] = ss
        ck(f'{n}: exact ordered domains', len(ss) == n and all(
            int(row['index']) == i and F(row['q_lo']) == F(i, n)
            and F(row['q_hi']) == F(i + 1, n) for i, row in enumerate(ss)))
        ck(f'{n}: displayed enclosure signs and targets', all(
            D(row['lower']) <= D(row['upper']) < D('-0.00001') for row in ss))
        worst = max(ss, key=lambda row: D(row['upper']))
        run = runs[j]
        ck(f'{n}: summary extrema and configuration',
           int(run['worst_slab_index']) == int(worst['index'])
           and D(run['worst_phi_second_lower']) == D(worst['lower'])
           and D(run['worst_phi_second_upper']) == D(worst['upper'])
           and int(run['terminal_rectangles']) == n * m
           and int(run['q_slabs']) == n and int(run['x_panels']) == m
           and int(run['bits']) == 384)
        ck(f'{n}: JSON CSV agreement', all(
            str(summary['arb']['runs'][j][key]) == value for key, value in run.items()))
        ck(f'{n}: summary booleans', boolean(run['proves_strict_concavity'])
           and boolean(run['proves_target_minus_1_over_100000']))
    ck('displayed worst bounds tighten', all(
        D(runs[i + 1]['worst_phi_second_upper']) < D(runs[i]['worst_phi_second_upper'])
        for i in range(2)))
    for j, row in enumerate(endpoints):
        ck(f'endpoint {j}: displayed widths and targets',
           int(row['x_panels']) == [4, 8, 16][j]
           and int(row['bits']) == 384 and D(row['upper']) > D(row['lower']) > D('0.00025')
           and D(row['width']) == D(row['upper']) - D(row['lower'])
           and boolean(row['proves_phi_one_positive'])
           and boolean(row['proves_phi_one_gt_1_over_4000']))
        ck(f'endpoint {j}: JSON CSV agreement', all(
            str(summary['arb']['endpoint_runs'][j][key]) == value
            for key, value in row.items()))
    ck('displayed endpoint intervals nested', all(
        contains(pair(endpoints[i]), pair(endpoints[i + 1])) for i in range(2)))

    mp_rows = rows(mpfr / 'forward_384/concavity_slab_summary.csv')
    mp = {int(row['index']): row for row in mp_rows}
    legacy = doc(root / 'research/confocal_peabody_analytic_compression/data/'
                'certificate_80dps/peabody_concavity_certificate.json')
    legacy_rows = legacy['concavity']['slabs']
    old = {int(row['index']): row for row in legacy_rows}
    comparisons = rows(recon / 'slabwise_enclosure_comparison.csv')
    ck('32 complete baseline inputs and aggregate rows',
       len(mp_rows) == len(legacy_rows) == len(comparisons) == 32
       and set(mp) == set(old) == set(range(32)))
    for i, row in enumerate(comparisons):
        a = tuple(D(mp[i]['phi_second_' + side]) for side in ('lower', 'upper'))
        b = tuple(D(old[i]['phi_second'][side]) for side in ('lower', 'upper'))
        ck(f'aggregate {i}: domains and baseline inputs', int(row['index']) == i
           and F(row['q_lo']) == F(i, 32) and F(row['q_hi']) == F(i + 1, 32)
           and pair(row, 'mpfr_') == a and pair(row, 'mpmath_') == b)
        ck(f'aggregate {i}: baseline containment', overlap(a, b) and contains(a, b)
           and boolean(row['mpmath_mpfr_intersect'])
           and boolean(row['mpfr_contains_mpmath']))
        for n, m in configurations:
            chunk = slabs[n][i * (n // 32):(i + 1) * (n // 32)]
            aggregate = (min(D(s['lower']) for s in chunk), max(D(s['upper']) for s in chunk))
            prefix = f'arb_{n}x{m}_'
            ck(f'aggregate {i} {n}: exact displayed aggregation and booleans',
               pair(row, prefix) == aggregate
               and D(row[prefix + 'width']) == aggregate[1] - aggregate[0]
               and boolean(row[prefix + 'intersects_mpfr']) == overlap(aggregate, a)
               and boolean(row[prefix + 'contains_mpfr']) == contains(aggregate, a))
            ck(f'aggregate {i} {n}: overlaps MPFR', overlap(aggregate, a))

    baseline = doc(recon / 'baseline_interval_comparison.json')
    baseline_rows = rows(recon / 'baseline_interval_comparison.csv')
    ck('32 baseline comparison rows', len(baseline_rows) == 32)
    lower_differences, upper_differences = [], []
    for i, row in enumerate(baseline_rows):
        a = tuple(D(mp[i]['phi_second_' + s]) for s in ('lower', 'upper'))
        b = tuple(D(old[i]['phi_second'][s]) for s in ('lower', 'upper'))
        lo, hi = abs(a[0] - b[0]), abs(a[1] - b[1])
        lower_differences.append(lo)
        upper_differences.append(hi)
        ck(f'baseline {i}: all displayed fields', int(row['index']) == i
           and pair(row, 'mpfr_') == a and pair(row, 'mpmath_') == b
           and D(row['absolute_lower_difference']) == lo
           and D(row['absolute_upper_difference']) == hi
           and boolean(row['intervals_intersect']) == overlap(a, b)
           and boolean(row['mpmath_contains_mpfr']) == contains(b, a)
           and boolean(row['mpfr_contains_mpmath']) == contains(a, b))
    ck('baseline maximum displayed differences',
       D(baseline['comparison']['max_absolute_lower_endpoint_difference']) == max(lower_differences)
       and D(baseline['comparison']['max_absolute_upper_endpoint_difference']) == max(upper_differences))
    mp_json = doc(mpfr / 'forward_384/peabody_mpfr_concavity_certificate.json')
    for kind in ('direct_mpfr', 'legacy_mpmath_iv'):
        reported = summary['archived_endpoint_interval_implementations'][kind]
        if kind == 'direct_mpfr':
            lo, hi = [mp_json['endpoint']['phi_one_' + s] for s in ('lower', 'upper')]
            worst = max(D(row['phi_second_upper']) for row in mp.values())
        else:
            lo, hi = [legacy['endpoint']['phi_one_enclosure'][s] for s in ('lower', 'upper')]
            worst = max(D(row['phi_second']['upper']) for row in old.values())
        ck(kind + ': summary matches inputs', D(reported['endpoint_lower']) == D(lo)
           and D(reported['endpoint_upper']) == D(hi)
           and D(reported['worst_phi_second_upper']) == worst)
    for side in ('lower', 'upper'):
        ck('baseline endpoint displayed difference ' + side,
           abs(D(mp_json['endpoint']['phi_one_' + side])
               - D(legacy['endpoint']['phi_one_enclosure'][side]))
           == D(baseline['comparison']['endpoint_' + side + '_difference']))

    reconstructed, authoritative, authoritative_slabs = [], {}, {}
    for name, bits, order in [('forward_384', 384, 'forward'),
                               ('forward_512', 512, 'forward'),
                               ('reverse_384', 384, 'reverse')]:
        directory = arb / name
        cert = doc(directory / 'peabody_arb_concavity_certificate.json')
        slab_rows = rows(directory / 'concavity_slab_summary.csv')
        authoritative[name] = cert
        authoritative_slabs[name] = {int(row['index']): row for row in slab_rows}
        terminal = rows(directory / 'concavity_terminal_boxes.csv')
        endpoint_rows = rows(directory / 'endpoint_terminal_boxes.csv')
        ck(name + ': targets configuration and environment', cert['pass'] is True
           and cert['classification'] == 'GO_PEABODY_ARB_FLINT_CERTIFICATE'
           and cert['proof_status'] == 'CERTIFIED'
           and cert['environment']['precision_bits'] == bits
           and cert['environment']['python_flint_distribution'] == '0.9.0'
           and cert['subdivision_order'] == order and cert['correction_sign'] == 1
           and cert['terminal_rectangles'] == 324
           and cert['endpoint']['target'] == '1/4000'
           and cert['concavity']['target'] == '-1/100000')
        ck(name + ': EXACT BINARY publication bounds',
           binary(cert['endpoint']['phi_one_enclosure']['lower_binary']) > F(1, 4000)
           and binary(cert['concavity']['worst_phi_second_upper_binary']) < -F(1, 100000))
        ck(name + ': EXACT BINARY domain positivity',
           len(cert['domain_diagnostics']) == 7 and all(v['finite'] and v['strictly_positive']
           and binary(v['lower_binary']) > 0 for v in cert['domain_diagnostics'].values()))
        ck(name + ': all output hashes', hashes(directory))
        ck(name + ': terminal and slab counts', len(terminal) == 320
           and len(endpoint_rows) == 4 and len(slab_rows) == 32
           and set(authoritative_slabs[name]) == set(range(32)))
        ck(name + ': exact endpoint panel domains', all(int(row['x_panel_index']) == i
           and F(row['x_lo']) == F(i, 4) and F(row['x_hi']) == F(i + 1, 4)
           for i, row in enumerate(endpoint_rows)))
        ck(name + ': exact endpoint contribution sums', all(
            contains(binary_pair(row, 'contribution'), add(binary_pair(row, 'midpoint_term'),
                                                          binary_pair(row, 'remainder_term')))
            for row in endpoint_rows))
        geometry, terms, targets, uppers = True, True, True, []
        for i in range(32):
            chunk = sorted((row for row in terminal if int(row['q_slab_index']) == i),
                           key=lambda row: int(row['x_panel_index']))
            geometry &= len(chunk) == 10 and all(
                F(row['q_lo']) == F(i, 32) and F(row['q_hi']) == F(i + 1, 32)
                and F(row['q_mid']) == F(2 * i + 1, 64)
                and int(row['x_panel_index']) == k and F(row['x_lo']) == F(k, 10)
                and F(row['x_hi']) == F(k + 1, 10) for k, row in enumerate(chunk))
            for row in chunk:
                for prefix in ('c_point', 'cq'):
                    terms &= contains(binary_pair(row, prefix + '_contribution'), add(
                        binary_pair(row, prefix + '_midpoint_term'),
                        binary_pair(row, prefix + '_remainder_term')))
            cm = tuple(sum(binary_pair(row, 'c_point_contribution')[s] for row in chunk)
                       for s in (0, 1))
            cq = tuple(sum(binary_pair(row, 'cq_contribution')[s] for row in chunk)
                       for s in (0, 1))
            c = add(cm, multiply((-F(1, 64), F(1, 64)), cq))
            phi = multiply(((1 + F(i, 32)) ** 3 / 32,
                            (1 + F(i + 1, 32)) ** 3 / 32), c)
            targets &= phi[1] < -F(1, 100000)
            uppers.append(phi[1])
        ck(name + ': exact domains of all 320 rectangles', geometry)
        ck(name + ': exact contribution sum enclosure of all 320 rectangles', terms)
        ck(name + ': all 32 EXACT reconstructed concavity targets', targets)
        reconstructed.append({'run': name, 'worst_reconstructed_upper_fraction': str(max(uppers)),
                              'worst_reconstructed_upper_decimal_approximation':
                              str(D(max(uppers).numerator) / D(max(uppers).denominator))})
        ck(name + ': displayed slab summary extrema and targets',
           D(cert['concavity']['worst_phi_second_upper'])
           == max(D(row['phi_second_upper']) for row in slab_rows)
           and all(D(row['phi_second_upper']) < D('-0.00001')
                   and boolean(row['below_negative_target']) for row in slab_rows))
    for name in ('forward_512', 'reverse_384'):
        a = authoritative['forward_384']['endpoint']['phi_one_enclosure']
        b = authoritative[name]['endpoint']['phi_one_enclosure']
        ck(name + ': EXACT BINARY endpoint overlap with forward 384', overlap(
            tuple(binary(a[s + '_binary']) for s in ('lower', 'upper')),
            tuple(binary(b[s + '_binary']) for s in ('lower', 'upper'))))
        ck(name + ': all 32 displayed slab overlaps with forward 384', all(overlap(
            tuple(D(authoritative_slabs['forward_384'][i]['phi_second_' + s])
                  for s in ('lower', 'upper')),
            tuple(D(authoritative_slabs[name][i]['phi_second_' + s])
                  for s in ('lower', 'upper'))) for i in range(32)))
    ck('all 32 forward 384 displayed slab overlaps with MPFR', all(overlap(
        tuple(D(authoritative_slabs['forward_384'][i]['phi_second_' + s])
              for s in ('lower', 'upper')),
        tuple(D(mp[i]['phi_second_' + s]) for s in ('lower', 'upper')))
        for i in range(32)))
    ck('forward 384 displayed endpoint overlap with MPFR', overlap(
        pair(authoritative['forward_384']['endpoint']['phi_one_enclosure']),
        tuple(D(mp_json['endpoint']['phi_one_' + s]) for s in ('lower', 'upper'))))
    for name in ('control_1x1', 'control_sign_mutation'):
        directory = arb / name
        cert = doc(directory / 'peabody_arb_concavity_certificate.json')
        ck(name + ': semantic rejection and expected exit', cert['pass'] is False
           and cert['proof_status'] == 'NOT_CERTIFIED'
           and cert['classification'] == 'NO_GO_PEABODY_ARB_FLINT_CERTIFICATE'
           and int(read(directory / 'EXPECTED_FAILURE_EXIT_CODE.txt')) == 2)
        ck(name + ': output hashes', hashes(directory))
        ck(name + ': intended adversarial configuration',
           (cert['correction_sign'] == 1 and cert['concavity']['q_slabs'] == 1
            and cert['concavity']['x_panels_per_slab'] == 1)
           if name == 'control_1x1' else cert['correction_sign'] == -1)
    # Hash inspected programs as provenance, without importing or executing them.
    for relative in ('arb/peabody_arb_concavity.py', 'python/run_arb_refinement_audit.py',
                     'python/compare_baseline_interval_enclosures.py',
                     'python/audit_arb_certificate.py'):
        read(checkpoint / relative)
    report = {
        'classification': 'ARCHIVED_RECONCILIATION_SEMANTIC_AUDIT_PASS'
        if all(checks.values()) else 'ARCHIVED_RECONCILIATION_SEMANTIC_AUDIT_FAIL',
        'pass': all(checks.values()), 'checks_count': len(checks),
        'scope': 'Archive semantic verification; no fresh Arb or MPFR special-function replay.',
        'trust_boundary': 'Exact Fraction reconstruction trusts the archived Arb terminal terms as '
        'enclosures of the analytic derivatives. It validates downstream arithmetic and targets.',
        'decimal_comparisons': 'Historical display diagnostics only; decimal strings are not '
        'assumed to be outward-rounded endpoint enclosures.',
        'refinement_slabs_verified': 224, 'aggregate_comparison_rows_verified': 32,
        'authoritative_terminal_rectangles_verified': 960, 'endpoint_panels_verified': 12,
        'publication_bounds': {'endpoint_lower': '1/4000', 'concavity_upper': '-1/100000'},
        'input_sha256': inputs, 'checks': checks,
        'failures': [name for name, value in checks.items() if not value],
        'reconstructed_concavity': reconstructed,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(report['classification'])
    print('checks:', len(checks), 'inputs:', len(inputs), 'failures:', report['failures'])
    return 0 if report['pass'] else 2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(audit(args.root, args.output))
