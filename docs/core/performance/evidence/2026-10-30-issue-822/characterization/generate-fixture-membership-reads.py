#!/usr/bin/env python3
"""Read --nocapture output of exact_empty_membership_reads_cover_each_candidate_mode.

Usage: generate-fixture-membership-reads.py LOG [REVISION OUTPUT_NAME]. Without the optional
arguments it regenerates the baseline file.
"""
import json
from pathlib import Path
import re
import sys

observations = {mode: [] for mode in ('instance', 'definition', 'mixed', 'no-op', 'graph-only')}
for mode, source, relationship, count in re.findall(
    r'\[fixture-membership\] mode=(\S+) source=(\S+) relationship=(\S+) requests=(\d+)',
    Path(sys.argv[1]).read_text(),
):
    observations[mode].append({'source': source, 'relationship': relationship, 'requests': int(count)})
if not all(observations.values()):
    raise ValueError('Missing fixture modes; run the characterization test with --nocapture')
revision, output = (sys.argv[2], sys.argv[3]) if len(sys.argv) > 2 else ('a3a280d1b59745038b63e9eb84f47b27b2193ff9', 'fixture-membership-reads.json')
report = {'production_revision': revision,
          'test': 'exact_empty_membership_reads_cover_each_candidate_mode',
          'scope': 'Assessment-only backend membership attempts after resetting the source counter; excludes setup and staging; not logical demand or guest measurements',
          'modes': observations}
Path(__file__).with_name(output).write_text(json.dumps(report, indent=2) + '\n')
