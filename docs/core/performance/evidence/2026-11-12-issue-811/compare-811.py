#!/usr/bin/env python3
"""Compare the #811 capture (scalar constraints active) with the #822 final capture.

Reads both captures without rewriting them and writes comparison.json beside this script.
Each side is one run of six samples per workload: "first" is sample 0 and "repeated" is the
median of samples 1-5. Latency is directional at this sample size; work counts are primary.
"""
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parent
BEFORE = ROOT.parent / '2026-10-30-issue-822/final/captured'
AFTER = ROOT / 'captured'
METRICS = {
    'command_us': 'commit-baseline.command_us',
    'guest_preparation_us': 'commit-construction.elapsed_us',
    'validation_ms': 'guest_commit.validation_ms',
    'pass_2_ms': 'guest_commit.pass_2_ms',
    'prepared_definitions': 'commit-preparation.requested_schema_products',
    'prepared_constraint_parameters': 'commit-preparation.prepared_constraint_parameters',
}
TOTALS = {
    'package_edge_requests': ('commit-preparation-edge.', 'requests'),
    'logical_requests': ('commit-logical-reads.', 'requests'),
    'assessment_link_queries': ('commit-assessment.', 'link_queries'),
    'assessment_exact_node_reads': ('commit-assessment.', 'exact_node_reads'),
}


def expanded(metrics):
    result = {name: metrics.get(key) for name, key in METRICS.items()}
    for name, (prefix, field) in TOTALS.items():
        keys = [k for k in metrics if k.startswith(prefix) and k.endswith('.' + field)]
        result[name] = sum(metrics[k] for k in keys) if keys else None
    return result


def summarize(directory):
    samples = json.loads((directory / 'measurements.json').read_text())['samples']
    rows = [(s['sample'], expanded(s['metrics'])) for s in samples]
    def median(group, name):
        values = [row[name] for _, row in group if row[name] is not None]
        return statistics.median(values) if values else None
    names = rows[0][1].keys()
    return {label: {name: median(group, name) for name in names}
            for label, group in [('first', [r for r in rows if r[0] == 0]),
                                 ('repeated', [r for r in rows if r[0] >= 1])]}


report = {'method': __doc__.strip(), 'workloads': {}}
for directory in sorted(p for p in AFTER.iterdir() if p.is_dir() and p.name != 'bootstrap'):
    meta = json.loads((directory / 'metadata.json').read_text())
    report['workloads'][directory.name] = {
        'after_revision': meta['revision'], 'status': meta['status'],
        'before': summarize(BEFORE / directory.name), 'after': summarize(directory)}
report['bootstrap_total_ms'] = {
    label: [run['total_ms'] for run in json.loads((path / 'bootstrap/measurements.json').read_text())]
    for label, path in [('before', BEFORE), ('after', AFTER)]}
(ROOT / 'comparison.json').write_text(json.dumps(report, indent=2) + '\n')

for group in ['repeated', 'first']:
    print(f'\n== {group} ==')
    print(f"{'workload':36}{'command ms':>20}{'prep ms':>18}{'validation ms':>18}{'logical req':>16}{'link q':>12}")
    for name, entry in report['workloads'].items():
        b, a = entry['before'][group], entry['after'][group]
        def pair(metric, scale=1.0, digits=0):
            if b[metric] is None or a[metric] is None:
                return 'n/a'
            return f"{b[metric]/scale:.{digits}f}->{a[metric]/scale:.{digits}f}"
        print(f"{name:36}{pair('command_us',1000):>20}{pair('guest_preparation_us',1000):>18}"
              f"{pair('validation_ms'):>18}{pair('logical_requests'):>16}{pair('assessment_link_queries'):>12}")
print('\nbootstrap total ms:', report['bootstrap_total_ms'])
print('prepared constraint parameters (first):',
      {n: e['after']['first']['prepared_constraint_parameters'] for n, e in report['workloads'].items()})
print('revisions:', {e['after_revision'] for e in report['workloads'].values()},
      'status:', {e['status'] for e in report['workloads'].values()})
