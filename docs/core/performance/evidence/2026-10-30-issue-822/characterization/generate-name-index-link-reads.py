#!/usr/bin/env python3
"""Extract NameIndexes membership misses from the retained inventory logs (not timings).

Run with the raw capture directory as the sole argument. Uses the same operation-boundary
records, source labels, sample markers and SHA-256 provenance as name-index-inventory.json.
"""
import collections
import hashlib
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
evidence = Path(__file__).resolve().parent.parent
previous = json.loads((evidence / 'diagnostics/name-index-inventory.json').read_text())
report = {k: previous[k] for k in ('revision', 'artifact')}
report['method'] = 'commit-operation-read operation=NameIndexes; relationship != Node; outcome != hit'
report['captures'] = {}
for name, capture in previous['captures'].items():
    path = root / (name + '.log')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != capture['log_sha256']:
        raise ValueError(f'{path}: does not match original inventory SHA-256')
    text = path.read_text()
    labels = {}
    for match in re.finditer(r'holon_id: Local\(LocalId \{ bytes: "([0-9a-f]+)" \}\), smart_property_values: Some\(\{([^}]+)\}', text):
        key = re.search(r'PropertyName\(MapString\("Key"\)\): StringValue\(MapString\("([^"]+)"\)\)', match[2])
        if key:
            labels[match[1]] = key[1]
    samples = []
    sample = None
    for line in text.splitlines():
        fields = dict(re.findall(r'([a-zA-Z_0-9]+)=([^\s]+)', line))
        if '[commit-baseline]' in line and 'sample_start' in fields:
            sample = {'sample': int(fields['sample_start']), 'reads': collections.Counter(), 'records': 0}
            samples.append(sample)
        if sample is None:
            continue
        if '[commit-operation-read]' in line and fields.get('operation') == 'NameIndexes':
            sample['records'] += 1
            if fields['relationship'] != 'Node' and fields['outcome'] != 'hit':
                sample['reads'][(fields['source'], fields['relationship'], fields['outcome'])] += int(fields['requests'])
        if '[commit-baseline]' in line and 'sample_end' in fields:
            sample = None
    output = []
    for sample in samples:
        if not sample['records']:
            raise ValueError(f'{path}: sample has no detailed operation observations')
        rows = [{'source': source, 'key': labels.get(source[-78:]), 'relationship': relationship,
                 'outcome': outcome, 'requests': count}
                for (source, relationship, outcome), count in sorted(sample['reads'].items())]
        output.append({'sample': sample['sample'], 'operation_records': sample['records'],
                       'membership_misses': sum(row['requests'] for row in rows),
                       'by_relationship': dict(sorted(collections.Counter({relationship: sum(row['requests'] for row in rows if row['relationship'] == relationship) for relationship in {row['relationship'] for row in rows}}).items())),
                       'sources': rows})
    report['captures'][name] = {'log_sha256': digest, 'samples': output}
(evidence / 'diagnostics/name-index-link-reads.json').write_text(json.dumps(report, indent=2) + '\n')
for name, capture in report['captures'].items():
    for sample in capture['samples']:
        print(name, sample['sample'], sample['by_relationship'])
