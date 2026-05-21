---
name: map-dev-tracking-sheet
description: Updates and archives the MAP Dev Tracking Google Sheet using bundled Google Sheets and Drive helpers. Use when the user asks to add, edit, upsert, reconcile, archive, snapshot, version, or verify MAP development tracking rows or release metrics in the MAP Dev Tracking Google Sheet.
---

# MAP Dev Tracking Sheet

Use this skill to make direct, auditable updates to the MAP Dev Tracking Google Sheet.

## Required context

- The default spreadsheet is the MAP Dev Tracking Google Sheet:
  `https://docs.google.com/spreadsheets/d/1jiDhstMzCUkke72ePHdmQuIbpZAIlR25JMRB6JuDiE8/edit`
- Use `MAP_DEV_TRACKING_SPREADSHEET_ID` or `--spreadsheet-id` only when the user explicitly points to a different sheet.
- Use credentials from `~/.config/map-dev-tracking/service-account.json`, `GOOGLE_SHEETS_ACCESS_TOKEN`, `GOOGLE_APPLICATION_CREDENTIALS`, or an authenticated `gcloud` session.
- Never invent row keys, statuses, dates, issue numbers, PR links, owners, or notes. Read the sheet or ask the user when a value is ambiguous.
- Keep secrets and service account JSON files outside this repository.
- Before material release updates, duplicate the live worksheets in place with a release label such as `pre-v1.4`.
- Use whole-spreadsheet Drive copies only when the authenticated account can create Drive files; service accounts may fail with Drive storage quota errors.
- Keep the live worksheets first in this order when archives exist: `Weekly Rollups`, `Completion Tracker`, `Waves Progress`.
- Prefer `upsert-row` for tracking rows because it reads headers, finds the row by key, and updates named columns.
- When syncing `Waves Progress` from the roadmap plan, do not revise rows where `Status` is `Done`; those rows are historical ledger entries.
- For non-`Done` rows, update only plan-owned columns:
  `Wave`, `Track`, `PR`, `Description`, `Estimate Points`, `Confidence`, `Blocking Dependency`, `Notes`, and `Last Updated`.
- Treat these `Waves Progress` columns as manually owned and never overwrite them during roadmap sync:
  `Status`, `Owner`, `Points Completed`, `Week Completed`, and `Active Issue / PR`.
- If a v1.4 plan item is missing from `Waves Progress`, append a new row at the bottom with plan-owned columns populated, set `Status` to `Planned`, set `Owner` to `Unassigned`, set `Defined On` to today's date, and leave `Points Completed`, `Week Completed`, `Active Issue / PR`, and `Last Updated` blank unless the user explicitly provides values.

## Workflow

1. Identify the target worksheet, key column, key value, and columns to update.
2. Read the relevant area before editing:

   ```bash
   python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py get --range "'Completion Tracker'!A1:Z50"
   ```

3. For material release changes, archive the live worksheets first:

   ```bash
   python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py archive-worksheet --worksheet "Completion Tracker" --label pre-v1.4
   ```

4. Preview complex edits with `--dry-run` when practical.
5. Apply the smallest update that satisfies the request.
6. Re-read the changed row or range and report the confirmed values back to the user.

## Common commands

List worksheets:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py list-worksheets
```

Keep the live worksheets as the first three tabs:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py reorder-worksheets \
  --worksheet "Weekly Rollups" \
  --worksheet "Completion Tracker" \
  --worksheet "Waves Progress"
```

Duplicate one worksheet inside the active spreadsheet:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py archive-worksheet \
  --worksheet "Completion Tracker" \
  --label pre-v1.4
```

Copy the whole spreadsheet when Drive file creation is available:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py copy-spreadsheet --label pre-v1.4
```

Update or create a row by matching a key column:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py upsert-row \
  --worksheet "Completion Tracker" \
  --key-column "Issue" \
  --key-value "473" \
  --set "Status=Done" \
  --set "PR=https://github.com/evomimic/map-holons/pull/473"
```

Append a row:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py append-row \
  --worksheet "Completion Tracker" \
  --row-json '["473","Done","https://github.com/evomimic/map-holons/pull/473"]'
```

Update an exact A1 range:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py update-range \
  --range "'Completion Tracker'!C12:D12" \
  --values-json '[["Done","2026-05-21"]]'
```

## Setup and troubleshooting

See [Google Sheets setup](references/google-sheets-setup.md) for credential setup, environment variables, examples, and common API errors.
