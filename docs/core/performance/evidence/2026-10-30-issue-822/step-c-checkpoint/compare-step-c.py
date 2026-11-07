#!/usr/bin/env python3
"""Compare the Step C checkpoint with the core lookup reuse foundation capture.

Reads both captures without rewriting them and writes comparison.json beside this script.
Reports sample 0, sample 1, and the median of samples 2-5. Checks moved into construction
in Step C, so operation totals are reported beside phase totals.
"""
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parent
CAPTURES = {'foundation_core_lookup_reuse': ROOT.parent / 'foundation-checkpoint/captured-fed00431',
            'step_c': ROOT / 'captured'}
WORKLOADS = ['usage', 'no-op', 'mixed', 'shared-type']
OP = 'commit-preparation-operation.'
METRICS = {
    'command_us': 'commit-baseline.command_us',
    'guest_preparation_us': 'commit-construction.elapsed_us',
    'validation_ms': 'guest_commit.validation_ms',
    'requested_schema_products': 'commit-preparation.requested_schema_products',
    'retained_identities': 'commit-preparation.distinct_content',
    'identity_role_visits': 'commit-preparation.identity_role_visits',
    'derived_property_type_invocations': OP + 'DerivedAcquisition.PropertyType.invocations',
    'derived_value_type_invocations': OP + 'DerivedAcquisition.ValueType.invocations',
    'fresh_schema_invocations': OP + 'FreshEffectiveSchema.PreparedDefinition.invocations',
    'key_evidence_us': OP + 'saved_lineage_roots_by_key.key-evidence.elapsed_us',
    'link_prefix_cost_us': 'commit-read-cost.Construction.LinkPrefix.elapsed_us',
    'link_batched_prefix_cost_us': 'commit-read-cost.Construction.LinkBatchedPrefix.elapsed_us',
    'link_count_probe_cost_us': 'commit-read-cost.Construction.LinkCountProbe.elapsed_us',
    'link_single_scan_cost_us': 'commit-read-cost.Construction.LinkSingleScan.elapsed_us',
    'other_construction_cost_us': 'commit-read-cost.Construction.OtherConstruction.elapsed_us',
    'pass_2_ms': 'guest_commit.pass_2_ms',
    'registry_population': 'commit-registry.population',
}
OPERATIONS = ['MembershipPrefetch', 'Navigation', 'NameIndexes', 'ContentRetention', 'StructuralDiagnosis',
              'DerivedAcquisition', 'FreshEffectiveSchema', 'ContractChecks', 'BindingRoles']


def totals(metrics, prefix, field):
    keys = [k for k in metrics if k.startswith(prefix) and k.endswith('.' + field)]
    return sum(metrics[k] for k in keys) if keys else None


def expanded(metrics):
    result = {name: metrics.get(key) for name, key in METRICS.items()}
    result['package_edge_requests'] = totals(metrics, 'commit-preparation-edge.', 'requests')
    result['logical_requests'] = totals(metrics, 'commit-logical-reads.', 'requests')
    result['assessment_backend_calls'] = totals(metrics, 'commit-assessment.', 'backend_calls')
    result['assessment_link_queries'] = totals(metrics, 'commit-assessment.', 'link_queries')
    result['assessment_exact_node_reads'] = totals(metrics, 'commit-assessment.', 'exact_node_reads')
    for operation in OPERATIONS:
        for field in ['elapsed_us', 'link_queries']:
            result[f'{operation}_{field}'] = totals(metrics, OP + operation + '.', field) or 0
    return result


def groups(samples):
    rows = [expanded(sample['metrics']) for sample in samples]
    median = {}
    for name in rows[0]:
        values = [row[name] for row in rows[2:6] if row[name] is not None]
        median[name] = statistics.median(values) if values else None
    return {'sample_0': rows[0], 'sample_1': rows[1], 'samples_2_5_median': median}


report = {'method': 'One run, six samples per workload; samples 2-5 medians are directional.', 'workloads': {}}
for workload in WORKLOADS:
    entry = {}
    for label, directory in CAPTURES.items():
        meta = json.loads((directory / workload / 'metadata.json').read_text())
        data = json.loads((directory / workload / 'measurements.json').read_text())
        assert meta['status'] == '' and [s['sample'] for s in data['samples']] == list(range(6))
        entry[label] = {'revision': meta['revision'], 'preparation_substrate': meta['preparation_substrate'],
                        'captured_at_utc': meta['captured_at_utc'], **groups(data['samples'])}
    report['workloads'][workload] = entry
(ROOT / 'comparison.json').write_text(json.dumps(report, indent=2) + '\n')
