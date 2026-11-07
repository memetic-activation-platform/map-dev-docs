#!/usr/bin/env python3
"""Write the full fixture membership removal set across the foundation merge and Step C.

Reads the baseline, foundation and Step C inventories beside this script and writes
fixture-membership-reads-diff.json. Pairs are (source, relationship); counts are requests.
"""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INVENTORIES = {'baseline': 'fixture-membership-reads.json', 'foundation': 'fixture-membership-reads-foundation.json',
               'step_c': 'fixture-membership-reads-step-c.json'}


def load(name):
    report = json.loads((ROOT / name).read_text())
    return report['production_revision'], {mode: {(r['source'], r['relationship']): r['requests'] for r in rows}
                                           for mode, rows in report['modes'].items()}


loaded = {label: load(name) for label, name in INVENTORIES.items()}
inventories = {label: modes for label, (_, modes) in loaded.items()}


def pairs(keys):
    return [{'source': source, 'relationship': relationship} for source, relationship in sorted(keys)]


report = {'revisions': {label: revision for label, (revision, _) in loaded.items()}, 'modes': {}}
for mode in inventories['baseline']:
    baseline, foundation, step_c = (inventories[label][mode] for label in ('baseline', 'foundation', 'step_c'))
    removed = set(foundation) - set(step_c)
    report['modes'][mode] = {
        'pairs': {label: len(inventories[label][mode]) for label in INVENTORIES},
        'requests': {label: sum(inventories[label][mode].values()) for label in INVENTORIES},
        'foundation_added': pairs(set(foundation) - set(baseline)),
        'step_c_added': pairs(set(step_c) - set(foundation)),
        'step_c_removed_by_relationship': dict(Counter(relationship for _, relationship in removed).most_common()),
        'step_c_removed': pairs(removed),
    }
(ROOT / 'fixture-membership-reads-diff.json').write_text(json.dumps(report, indent=2) + '\n')
