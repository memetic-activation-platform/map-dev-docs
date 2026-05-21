# Google Sheets Setup

This skill updates the MAP Dev Tracking Google Sheet through the Google Sheets API. It can duplicate worksheets in place before material release updates, and can also copy the whole spreadsheet through the Google Drive API when the authenticated account can create Drive files. The helper script does not store credentials and does not require secrets in this repository.

## Default sheet

The default target is the MAP Dev Tracking Google Sheet:

```text
https://docs.google.com/spreadsheets/d/1jiDhstMzCUkke72ePHdmQuIbpZAIlR25JMRB6JuDiE8/edit
```

The helper can run against that sheet without a spreadsheet environment variable.

## Optional environment override

Set this only when targeting another sheet:

```bash
export MAP_DEV_TRACKING_SPREADSHEET_ID="spreadsheet-id-from-the-google-sheets-url"
```

The spreadsheet ID is the long value between `/d/` and `/edit` in a Google Sheets URL. A `--spreadsheet-id` argument overrides both the default sheet and the environment variable.

## Authentication options

Use one of these options.

### Option A: Service account

This is the best repeatable setup for agents.

1. Create or choose a Google Cloud project.
2. Enable the Google Sheets API.
3. Enable the Google Drive API if you want full-spreadsheet release archives.
4. Create a service account and download its JSON key to a private path outside the repo, such as `~/.config/map-dev-tracking/service-account.json`.
5. Share the MAP Dev Tracking Google Sheet with the service account email as an editor.
6. Export:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/map-dev-tracking/service-account.json"
   ```

The helper also checks `~/.config/map-dev-tracking/service-account.json` automatically when `GOOGLE_APPLICATION_CREDENTIALS` is not set. It uses `google-auth` when this option is selected. If it is missing, install it in the local Python environment:

```bash
python3 -m pip install google-auth requests
```

### Option B: Access token

Provide a Sheets-capable OAuth access token directly:

```bash
export GOOGLE_SHEETS_ACCESS_TOKEN="ya29..."
```

This is useful for short-lived manual sessions.

For `copy-spreadsheet`, the token must also have Google Drive permission.

### Option C: gcloud fallback

If `gcloud` is installed and authenticated, the helper will try:

```bash
gcloud auth print-access-token
```

or:

```bash
gcloud auth application-default print-access-token
```

If Google returns a permissions or insufficient-scope error, use a service account or provide `GOOGLE_SHEETS_ACCESS_TOKEN` with Sheets API write scope. Full-spreadsheet archives also require Drive permission.

## Helper script examples

Duplicate one worksheet inside the active spreadsheet before a material release update:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py archive-worksheet \
  --worksheet "Completion Tracker" \
  --label pre-v1.4
```

Create a whole-spreadsheet archive when Drive file creation is available:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py copy-spreadsheet --label pre-v1.4
```

List worksheet names and IDs:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py list-worksheets
```

Keep live worksheets before archive worksheets:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py reorder-worksheets \
  --worksheet "Weekly Rollups" \
  --worksheet "Completion Tracker" \
  --worksheet "Waves Progress"
```

Read a range:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py get --range "'Completion Tracker'!A1:Z25"
```

Preview a named-column upsert:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py --dry-run upsert-row \
  --worksheet "Completion Tracker" \
  --key-column "Issue" \
  --key-value "473" \
  --set "Status=Done"
```

Use JSON from a file:

```bash
python3 .agents/skills/map-dev-tracking-sheet/scripts/update_tracking_sheet.py update-range \
  --range "'Completion Tracker'!A2:C2" \
  --values-json @/tmp/map-dev-tracking-values.json
```

## Troubleshooting

- `403` means the token cannot edit the sheet, the API is not enabled, or the service account has not been shared on the sheet.
- Drive copy failures usually mean the Google Drive API is disabled, the token lacks Drive permission, the authenticated identity cannot create files in the source folder, or the service account does not have Drive storage quota. Use `archive-worksheet` as the service-account-friendly fallback.
- `404` usually means the spreadsheet ID is wrong or the authenticated identity cannot see the sheet.
- `Missing header` means the worksheet header row does not contain the column name passed to `--key-column` or `--set`.
- Keep all credential files out of git. Do not place service account JSON under `.agents/skills/`.
