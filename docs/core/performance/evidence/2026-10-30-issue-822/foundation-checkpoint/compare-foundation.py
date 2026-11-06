#!/usr/bin/env python3
"""Compare the corrected Step A checkpoint with the foundation checkpoint.

Reads both captures without rewriting them and writes comparison.json beside this script.
Reports sample 0, sample 1, and the median of samples 2-5. Instrumentation differs
(822-v2 -> 822-v3), so a metric absent from one capture stays null rather than zero.
"""
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parent
CAPTURES = {'step_a': ROOT.parent / 'step-a-checkpoint/corrected', 'foundation': ROOT / 'captured'}
WORKLOADS = ['usage', 'no-op', 'mixed', 'shared-type']
OP = 'commit-preparation-operation.'
METRICS = {
    'command_us': 'commit-baseline.command_us',
    'guest_preparation_us': 'commit-construction.elapsed_us',
    'prepared_products_us': 'commit-assessment.PreparedProducts.elapsed_us',
    'package_validation_us': 'commit-assessment.PackageValidation.elapsed_us',
    'derived_property_type_us': OP + 'DerivedAcquisition.PropertyType.elapsed_us',
    'derived_property_type_invocations': OP + 'DerivedAcquisition.PropertyType.invocations',
    'derived_property_type_link_queries': OP + 'DerivedAcquisition.PropertyType.link_queries',
    'derived_value_type_us': OP + 'DerivedAcquisition.ValueType.elapsed_us',
    'derived_value_type_invocations': OP + 'DerivedAcquisition.ValueType.invocations',
    'derived_value_type_link_queries': OP + 'DerivedAcquisition.ValueType.link_queries',
    'fresh_schema_us': OP + 'FreshEffectiveSchema.PreparedDefinition.elapsed_us',
    'fresh_schema_invocations': OP + 'FreshEffectiveSchema.PreparedDefinition.invocations',
    'name_indexes_us': OP + 'NameIndexes.PreparedDefinition.elapsed_us',
    'content_retention_us': OP + 'ContentRetention.SavedContent.elapsed_us',
    'category_routing_diagnosis_us': OP + 'StructuralDiagnosis.CategoryRouting.elapsed_us',
    'link_prefix_cost_us': 'commit-read-cost.Construction.LinkPrefix.elapsed_us',
    'other_construction_cost_us': 'commit-read-cost.Construction.OtherConstruction.elapsed_us',
    'host_snapshot_us': 'commit-host-snapshot.construction_us',
    'registry_capture_us': 'commit-registry-capture.elapsed_us',
    'registry_ingress_restoration_us': 'commit-registry-ingress.restoration_us',
    'registry_population': 'commit-registry.population',
    'prepared_definitions': 'commit-preparation.distinct_content',
}


def totals(metrics, prefix, field):
    keys = [k for k in metrics if k.startswith(prefix) and k.endswith('.' + field)]
    return sum(metrics[k] for k in keys) if keys else None


def expanded(metrics):
    result = {name: metrics.get(key) for name, key in METRICS.items()}
    result['package_edge_requests'] = totals(metrics, 'commit-preparation-edge.', 'requests')
    result['logical_requests'] = totals(metrics, 'commit-logical-reads.', 'requests')
    result['assessment_backend_calls'] = totals(metrics, 'commit-assessment.', 'backend_calls')
    result['assessment_exact_node_reads'] = totals(metrics, 'commit-assessment.', 'exact_node_reads')
    for operation in ['structural_diagnoses', 'schema_resolution_requests', 'schema_builder_attempts',
                      'saved_restoration_attempts', 'derived_builder_attempts', 'frozen_product_reuses',
                      'registry_lookups', 'registry_hits']:
        result[operation] = totals(metrics, 'commit-derivation.', operation)
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
        entry[label] = {'revision': meta['revision'], 'instrumentation': meta['instrumentation'],
                        'captured_at_utc': meta['captured_at_utc'], **groups(data['samples'])}
    report['workloads'][workload] = entry
(ROOT / 'comparison.json').write_text(json.dumps(report, indent=2) + '\n')
