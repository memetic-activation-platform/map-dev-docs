#!/usr/bin/env python3
"""Read --nocapture output of exact_empty_membership_reads_cover_each_candidate_mode."""
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
report = {'production_revision': 'a3a280d1b59745038b63e9eb84f47b27b2193ff9',
          'test': 'exact_empty_membership_reads_cover_each_candidate_mode',
          'scope': 'Assessment-only backend membership attempts after resetting the source counter; excludes setup and staging; not logical demand or guest measurements',
          'modes': observations}
Path(__file__).with_name('fixture-membership-reads.json').write_text(json.dumps(report, indent=2) + '\n')
