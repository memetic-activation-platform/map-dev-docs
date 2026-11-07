#!/usr/bin/env python3
"""Summarize the operation-scoped logical read inventory in usage.log (not timings).

Writes summary.json beside this script. A non-hit outcome is a logical cache miss; key
lookups and other reads outside the logical cache do not appear in this inventory.
"""
import collections
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
LOG = ROOT / 'usage.log'
ANSI = re.compile(r'\x1b\[[0-9;]*m')

samples, sample = [], None
for line in LOG.read_text(errors='replace').splitlines():
    line = ANSI.sub('', line)
    fields = dict(re.findall(r'([a-zA-Z_0-9]+)=([^\s]+)', line))
    if '[commit-baseline]' in line and 'sample_start' in fields:
        sample = {'sample': int(fields['sample_start']), 'condition': fields['condition'], 'reads': []}
        samples.append(sample)
    if sample is None:
        continue
    if '[commit-operation-read]' in line:
        sample['reads'].append(fields)
    if '[commit-baseline]' in line and 'sample_end' in fields:
        sample = None

report = {'revision': (ROOT / 'revision.txt').read_text().strip(),
          'log_sha256': hashlib.sha256(LOG.read_bytes()).hexdigest(),
          'method': 'commit-read-inventory build; usage workload; two samples; [commit-operation-read]',
          'samples': []}
for sample in samples:
    operations = collections.defaultdict(list)
    for read in sample['reads']:
        operations[f"{read['operation']}.{read['role']}"].append(read)
    summary = {}
    for name, reads in sorted(operations.items()):
        misses = [r for r in reads if r['outcome'] != 'hit']
        per_invocation = collections.Counter()
        for read in misses:
            if read['relationship'] != 'Node':
                per_invocation[read['invocation']] += int(read['requests'])
        by_relationship = collections.Counter()
        for read in misses:
            by_relationship[read['relationship']] += int(read['requests'])
        summary[name] = {
            'invocations': len({r['invocation'] for r in reads}),
            'requests': sum(int(r['requests']) for r in reads),
            'misses': sum(int(r['requests']) for r in misses),
            'misses_by_relationship': dict(by_relationship.most_common()),
            'distinct_link_miss_sources': len({r['source'] for r in misses if r['relationship'] != 'Node'}),
            'link_misses_per_invocation': dict(sorted(collections.Counter(per_invocation.values()).items())),
        }
    report['samples'].append({'sample': sample['sample'], 'condition': sample['condition'], 'operations': summary})
(ROOT / 'summary.json').write_text(json.dumps(report, indent=2) + '\n')
