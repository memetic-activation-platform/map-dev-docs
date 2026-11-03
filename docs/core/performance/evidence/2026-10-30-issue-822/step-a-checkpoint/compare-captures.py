#!/usr/bin/env python3
"""Verify and compare the bounded Step A captures; run from any directory.

Reads original captures without rewriting them. Re-parses retained git-ignored logs when
available, verifies per-sample package demand and actual registry conditions, and writes
comparison.json beside this script. Absent spans remain null, never measured zero.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parent
DOCS = next(p for p in ROOT.parents if (p / 'AGENTS.md').exists())
spec = importlib.util.spec_from_file_location('measure', DOCS.parent / 'map-holons/scripts/measure-commit-performance.py')
measure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(measure)
WORKLOADS = ['usage', 'no-op', 'mixed', 'shared-type']
GROUPS = {'first': [0], 'sample_1': [1], 'samples_2_5': [2, 3, 4, 5], 'repeated_1_5': [1, 2, 3, 4, 5]}
PHASES = measure.ASSESSMENT_PHASES

def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def expanded(sample):
    m = dict(sample['metrics'])
    for field in ['requests', 'membership_requests', 'content_requests', 'hits', 'misses']:
        m['assessment.logical.' + field] = sum(m[f'commit-logical-reads.{phase}.{field}'] for phase in PHASES)
    for field in ['backend_calls', 'link_queries', 'exact_node_reads']:
        m['assessment.' + field] = sum(m[f'commit-assessment.{phase}.{field}'] for phase in PHASES)
    for operation in measure.DERIVATION_OPERATIONS:
        m['assessment.derivation.' + operation] = sum(m[f'commit-derivation.{phase}.{operation}'] for phase in PHASES)
    return m

def selected(key):
    return (key.startswith(('assessment.', 'commit-construction.', 'commit-host-snapshot.',
                            'commit-logical-reads.', 'commit-derivation.', 'commit-assessment.', 'commit-preparation.'))
            or key == 'commit-baseline.command_us' or key == 'guest_commit.validation_ms'
            or (key.startswith('commit-preparation-operation.') and
                (key.endswith('.elapsed_us') or '.NameIndexes.' in key)))

def stats(values):
    return {'median': statistics.median(values), 'min': min(values), 'max': max(values)} if values else None

report = {'method': 'One run, six samples per workload. Samples 0 and 1 separate; samples 2–5 medians are directional only. Phase request/call counts may be summed; phase-local distinct memberships are never summed.',
          'workloads': {}}
for workload in WORKLOADS:
    captures = {}
    for label, directory in [('before', ROOT.parent / 'cache-10000-checkpoint' / workload),
                             ('after', ROOT / 'matched' / workload)]:
        metadata_path, measurements_path = directory / 'metadata.json', directory / 'measurements.json'
        meta = json.loads(metadata_path.read_text())
        data = json.loads(measurements_path.read_text())
        assert meta['status'] == '', (workload, label, 'dirty source')
        assert meta['guest_artifact_revision'] == meta['revision'], (workload, label, 'artifact revision label')
        assert meta['runs'] == 1 and meta['samples_per_run'] == 6
        assert [s['sample'] for s in data['samples']] == list(range(6))
        raw = directory / 'run-01.log'
        raw_state = {'state': 'unavailable'}
        if raw.exists():
            parsed = measure.summarize([raw], 6, meta['variant'], meta['assessment'], meta['mode'],
                                      meta['anchor_evidence_policy'], meta['instrumentation'],
                                      meta['preparation_substrate'], meta['host_snapshot_policy'],
                                      meta['expected_guest_cache_capacity'])
            assert parsed == data, (workload, label, 'parsed data differs')
            assert 'test result: ok. 1 passed' in raw.read_text()
            raw_state = {'state': 'reparsed and test outcome passed', 'sha256': fingerprint(raw)}
        captures[label] = {'meta': meta, 'data': data, 'raw': raw_state,
                           'sha256': {'metadata.json': fingerprint(metadata_path), 'measurements.json': fingerprint(measurements_path)}}
    before, after = captures['before'], captures['after']
    for key in ['mode', 'subjects_per_commit', 'expected_guest_cache_capacity', 'runtime_versions',
                'startup_timeout_secs', 'anchor_evidence_policy', 'instrumentation', 'variant', 'assessment',
                'rustc', 'cargo', 'platform', 'machine', 'cpu_count', 'guest_cache_state', 'session_product_reuse']:
        assert before['meta'][key] == after['meta'][key], (workload, key)
    # These pin the build/runtime foundation independently of the source implementation.
    for path in ['happ/Cargo.lock', 'host/Cargo.lock', 'Cargo.lock', 'flake.lock']:
        assert before['meta']['sha256'].get(path) == after['meta']['sha256'].get(path), (workload, path)
    assert before['meta']['preparation_substrate'] == 'broad-readiness'
    assert after['meta']['preparation_substrate'] == 'broad-preparation'
    pairs = []
    for old, new in zip(before['data']['samples'], after['data']['samples']):
        bm, am = old['metrics'], new['metrics']
        def package_edges(m):
            return {k: v for k, v in m.items() if k.startswith('commit-preparation-edge.') and not k.startswith('commit-preparation-edge.Readiness.')}
        assert package_edges(bm) == package_edges(am), (workload, old['sample'], 'package edges changed')
        for field in ['distinct_content', 'identity_role_visits', 'requested_schema_products', 'constructed_schema_products', 'package_roots', 'subjects', 'affected_schemas']:
            assert bm['commit-preparation.' + field] == am['commit-preparation.' + field], (workload, field)
        conditions = {k: v for k, v in bm.items() if k.startswith('commit-registry.') or
                      (k.startswith('commit-governor.') and not k.endswith('.sample'))}
        assert conditions == {k: v for k, v in am.items() if k.startswith('commit-registry.') or
                              (k.startswith('commit-governor.') and not k.endswith('.sample'))}
        assert not any(k.startswith(('commit-preparation-edge.Readiness.',
                                    'commit-preparation-operation.ReadinessDiscovery.',
                                    'commit-preparation-operation.DependencyGrouping.')) for k in am)
        assert 'commit-preparation-operation.InterpretationGuards.Candidate.elapsed_us' in am
        pairs.append({'sample': old['sample'], 'conditions': conditions,
                      'package_edge_requests': sum(v for k, v in package_edges(am).items() if k.endswith('.requests')),
                      'package_traversed_members': sum(v for k, v in package_edges(am).items() if k.endswith('.members')),
                      'removed_readiness_requests': sum(v for k, v in bm.items() if k.startswith('commit-preparation-edge.Readiness.') and k.endswith('.requests'))})
    groups = {}
    for group, indices in GROUPS.items():
        old = [expanded(before['data']['samples'][i]) for i in indices]
        new = [expanded(after['data']['samples'][i]) for i in indices]
        metrics = {}
        for key in sorted(set().union(*(m.keys() for m in old + new))):
            if not selected(key):
                continue
            ov, nv = [m[key] for m in old if key in m], [m[key] for m in new if key in m]
            bs, ns = stats(ov), stats(nv)
            delta = ns['median'] - bs['median'] if bs and ns else None
            percent = delta / bs['median'] * 100 if delta is not None and bs['median'] else None
            metrics[key] = {'before': bs, 'after': ns, 'delta': delta, 'percent': percent}
        groups[group] = metrics
    report['workloads'][workload] = {
        'before': {k: before['meta'][k] for k in ['revision', 'guest_artifact_revision', 'devdocs_revision', 'captured_at_utc']},
        'after': {k: after['meta'][k] for k in ['revision', 'guest_artifact_revision', 'devdocs_revision', 'captured_at_utc']},
        'artifact_sha256': {label: capture['meta']['sha256']['happ/workdir/map_holons.dna'] for label, capture in captures.items()},
        'capture_validation': {label: {'files': capture['sha256'], 'raw': capture['raw']} for label, capture in captures.items()},
        'per_sample_invariants': pairs, 'comparisons': groups}
(ROOT / 'comparison.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
for workload, result in report['workloads'].items():
    metrics = result['comparisons']['samples_2_5']
    print(workload)
    for key in ['commit-baseline.command_us', 'commit-construction.elapsed_us', 'assessment.logical.requests',
                'assessment.backend_calls', 'assessment.exact_node_reads', 'assessment.derivation.structural_diagnoses']:
        d = metrics[key]
        print(key, d['before']['median'], '->', d['after']['median'], d['percent'])
