# Visualizer evaluation comparison evidence

The source base is `1166e4bc`. Finding 3 was measured before commit and is now checkpointed as [a7667482](https://github.com/evomimic/map-holons/commit/a7667482fc561f753c16bf00781ac4c2906ef66b). `source-manifest.json` identifies the exact source files and built artifacts. `measurements.json` contains normalized values, source hashes, and measurement conditions. `composition-selected-markers.txt` preserves line-numbered measurement excerpts. Full raw logs remain in local temporary storage and are not committed.

Only passing runs 5, 6, and 7 enter the timing comparison. Earlier diagnostic runs are excluded. The separately preserved preference-replacement reproducer exposed two targets after replacing a saved preference; it is not part of these measured spans. Its broader persistence fix is separate from retained evaluation.
