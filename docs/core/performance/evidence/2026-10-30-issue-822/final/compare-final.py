#!/usr/bin/env python3
"""Compare the final #822 capture with the cache-99 baseline and the Step C smoke comparison point.

Reads captures without rewriting them and writes comparison.json beside this script. Baseline
values use all five runs; the final capture has one run. "Repeated" is the median of samples
1-5 in both, matching baseline-summary.md; samples 2-5 medians are also reported. The baseline
precedes the cache change, Step A and the #846 foundation, so this is the historical end-to-end
comparison; foundation -> final is available only for the smoke subset.
"""
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT.parent
RENAMED = {'registry-thirtytwo-affected-schema': 'registry-thirtytwo-bypass'}
METRICS = {
    'command_us': 'commit-baseline.command_us',
    'guest_preparation_us': 'commit-construction.elapsed_us',
    'validation_ms': 'guest_commit.validation_ms',
    'pass_2_ms': 'guest_commit.pass_2_ms',
    'host_snapshot_us': 'commit-host-snapshot.construction_us',
    'registry_population': 'commit-registry.population',
}


def totals(metrics, prefix, field):
    keys = [k for k in metrics if k.startswith(prefix) and k.endswith('.' + field)]
    return sum(metrics[k] for k in keys) if keys else None


def expanded(metrics, final):
    result = {name: metrics.get(key) for name, key in METRICS.items()}
    # The baseline predates requested_schema_products; its distinct_content counted prepared definitions.
    result['prepared_definitions'] = metrics.get('commit-preparation.requested_schema_products' if final
                                                 else 'commit-preparation.distinct_content')
    result['package_edge_requests'] = totals(metrics, 'commit-preparation-edge.', 'requests')
    result['logical_requests'] = totals(metrics, 'commit-logical-reads.', 'requests')
    result['assessment_link_queries'] = totals(metrics, 'commit-assessment.', 'link_queries')
    result['assessment_exact_node_reads'] = totals(metrics, 'commit-assessment.', 'exact_node_reads')
    for operation in ['saved_restoration_attempts', 'registry_hits', 'schema_builder_attempts',
                      'derived_builder_attempts', 'name_index_builds', 'structural_diagnoses']:
        result[operation] = totals(metrics, 'commit-derivation.', operation)
    return result


def median(rows, name):
    values = [row[name] for row in rows if row[name] is not None]
    return statistics.median(values) if values else None


def summarize(directory, final):
    samples = json.loads((directory / 'measurements.json').read_text())['samples']
    rows = {(s.get('run', 1), s['sample']): expanded(s['metrics'], final) for s in samples}
    first = [row for (_, sample), row in rows.items() if sample == 0]
    repeated = [row for (_, sample), row in rows.items() if sample >= 1]
    later = [row for (_, sample), row in rows.items() if sample >= 2]
    sample_1 = [row for (_, sample), row in rows.items() if sample == 1]
    names = next(iter(rows.values())).keys()
    return {group: {name: median(group_rows, name) for name in names}
            for group, group_rows in [('first', first), ('sample_1', sample_1),
                                      ('repeated_1_5', repeated), ('samples_2_5', later)]}


manifest = json.loads((ROOT / 'captured/manifest.json').read_text())
report = {'method': __doc__.strip(), 'final_manifest': manifest, 'workloads': {}}
for directory in sorted(path for path in (ROOT / 'captured').iterdir() if path.is_dir() and path.name != 'bootstrap'):
    workload = directory.name
    meta = json.loads((directory / 'metadata.json').read_text())
    assert meta['status'] == '' and meta['preparation_substrate'] == 'declared-demand'
    entry = {'final_revision': meta['revision'], 'baseline_name': RENAMED.get(workload, workload),
             'baseline': summarize(EVIDENCE / 'baseline' / RENAMED.get(workload, workload), False),
             'final': summarize(directory, True)}
    smoke = EVIDENCE / 'foundation-checkpoint/captured-fed00431' / workload
    if smoke.exists():
        entry['foundation_core_lookup_reuse'] = summarize(smoke, True)
    report['workloads'][workload] = entry
bootstrap = {label: [run['total_ms'] for run in json.loads((path / 'measurements.json').read_text())]
             for label, path in [('baseline', EVIDENCE / 'baseline/bootstrap'), ('final', ROOT / 'captured/bootstrap')]}
report['bootstrap_total_ms'] = {label: {'runs': runs, 'median': statistics.median(runs)} for label, runs in bootstrap.items()}
(ROOT / 'comparison.json').write_text(json.dumps(report, indent=2) + '\n')
