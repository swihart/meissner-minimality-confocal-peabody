#!/usr/bin/env python3
"""Validate the current review snapshot without rewriting historical manifests.

Archive verification is not a fresh Arb special-function evaluation. Passing
this gate does not assert completed external proofreading or submission approval.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from verify_archived_reconciliation import audit
from format_reconciliation_table import write_table

EXCLUDED = {'closeout/CURRENT_REVIEW_MANIFEST.json'}


def eligible(path):
    if path in EXCLUDED or '__pycache__' in Path(path).parts or Path(path).name == '.DS_Store':
        return False
    if path.startswith('manuscript/build-closeout/'):
        return path.endswith('/.gitignore')
    return True


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(repo):
    cp = repo / 'review/dcg-five-points'
    manifest = json.loads((cp/'closeout/CURRENT_REVIEW_MANIFEST.json').read_text())
    records = manifest['files']
    checks = {}
    checks['unique_manifest_paths'] = len(records) == len({r['path'] for r in records})
    actual = {str(p.relative_to(cp)) for p in cp.rglob('*') if p.is_file() and eligible(str(p.relative_to(cp)))}
    expected = {r['path'] for r in records}
    checks['exact_current_payload_set'] = actual == expected
    mismatches = [r['path'] for r in records if not (cp/r['path']).is_file() or sha(cp/r['path']) != r['sha256'] or (cp/r['path']).stat().st_size != r['bytes']]
    checks['all_current_hashes_and_sizes'] = not mismatches
    frozen = json.loads((repo/'PACKAGE_MANIFEST.json').read_text())
    checks['protected_frozen_50_files_unchanged'] = len(frozen['files']) == 50 and all(sha(repo/r['path']) == r['sha256'] for r in frozen['files'])
    progress = json.loads((cp/'data/reviewer_point_progress.json').read_text())
    checks['correct_review_branch'] = progress['branch'] == 'review/dcg-major-revision'
    checks['point_2_reconciled'] = progress['points']['2']['closed'] is True and progress['interval_enclosure_provenance_reconciled'] is True
    checks['external_review_and_submission_not_promoted'] = progress['external_review_recommended'] is True and progress['final_dcg_release_audit_pending'] is True
    with tempfile.TemporaryDirectory(prefix='peabody-closeout-') as temp:
        report = audit(repo, Path(temp)/'semantic.json')
        # Audit writes a reusable JSON; do not trust its Boolean without the checks.
        if not isinstance(report, dict):
            report = json.loads((Path(temp)/'semantic.json').read_text())
        checks['independent_archive_semantics'] = report['pass'] is True and bool(report['checks']) and all(report['checks'].values())
        table = Path(temp)/'table.tex'
        recon = json.loads((cp/'results/enclosure-reconciliation/enclosure_reconciliation.json').read_text())
        write_table(table, recon)
        checks['directed_display_table_exactly_regenerated'] = table.read_bytes() == (cp/'manuscript/generated_enclosure_reconciliation_closeout.tex').read_bytes()
        jet_output = Path(temp)/'derivative_jets.json'
        subprocess.run([sys.executable, str(cp/'python/verify_final_derivative_jets.py'),
                        '--repo-root', str(repo), '--output', str(jet_output)], check=True)
        jet = json.loads(jet_output.read_text())
        checks['final_derivative_jet_corroboration'] = (
            jet['pass'] is True and jet['checks_count'] == 286
            and len(jet['checks']) == 286 and all(jet['checks'].values())
            and jet['source_sha256'] == sha(cp/'arb/peabody_arb_concavity.py'))
    def binary(record):
        return Fraction(int(record['mantissa'])) * Fraction(2)**int(record['exponent'])
    decimal_lower = Fraction('0.000295140991676971')
    decimal_upper = Fraction('-0.000017928617848306')
    display_checks = []
    for run in ('forward_384', 'forward_512', 'reverse_384'):
        certificate = json.loads((cp/f'results/arb/{run}/peabody_arb_concavity_certificate.json').read_text())
        display_checks.append(binary(certificate['endpoint']['phi_one_enclosure']['lower_binary']) > decimal_lower > Fraction(1,4000))
        display_checks.append(binary(certificate['concavity']['worst_phi_second_upper_binary']) < decimal_upper < -Fraction(1,100000))
    checks['finite_display_bounds_outward_against_binary_archive'] = all(display_checks)
    checks['final_internal_audit_recorded_not_external'] = (
        progress.get('final_internal_mathematical_audit_completed') is True
        and progress.get('final_internal_mathematical_audit_classification') == 'PEABODY_FINAL_INTERNAL_MATHEMATICAL_AUDIT_PASS'
        and progress.get('external_review_completed') is False
        and progress.get('submission_ready') is False)
    manuscript = (cp/'manuscript/main_dcg_closeout_review.tex').read_text()
    checks['required_table_not_optional'] = r'\input{generated_enclosure_reconciliation_closeout.tex}' in manuscript and r'\IfFileExists' not in manuscript
    checks['publication_targets_unchanged'] = r'\frac1{4000}' in manuscript and r'-\frac1{100000}' in manuscript
    checks['code_and_ai_disclosures_present'] = r'\paragraph{Code and data availability.}' in manuscript and r'\paragraph{AI assistance.}' in manuscript
    checks['no_unsupported_correspondence_claim'] = 'We have sent' not in (cp/'notes/draft_response_to_referee.md').read_text()
    passed = all(checks.values())
    return {'classification': 'PEABODY_CURRENT_CLOSEOUT_ARCHIVE_AUDIT_PASS' if passed else 'PEABODY_CURRENT_CLOSEOUT_ARCHIVE_AUDIT_FAIL', 'pass': passed,
            'source_commit': manifest['source_commit'], 'current_payload_files': len(records), 'checks': checks,
            'missing': sorted(expected-actual), 'unexpected': sorted(actual-expected), 'hash_mismatches': mismatches,
            'semantic_check_count': len(report['checks']), 'fresh_arb_replay': False, 'r_runtime_executed': False,
            'derivative_jet_check_count': jet['checks_count'], 'finite_display_comparisons': len(display_checks),
            'internal_mathematical_audit_classification': progress['final_internal_mathematical_audit_classification'],
            'external_review_completed': False, 'submission_ready': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo-root', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = validate(args.repo_root.resolve())
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
    raise SystemExit(0 if result['pass'] else 2)
