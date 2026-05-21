#!/usr/bin/env python3
"""Update the MAP Dev Tracking Google Sheet through the Sheets API.

Usage examples:
  update_tracking_sheet.py get --range "'Completion Tracker'!A1:Z25"
  update_tracking_sheet.py reorder-worksheets --worksheet "Weekly Rollups" --worksheet "Completion Tracker" --worksheet "Waves Progress"
  update_tracking_sheet.py copy-spreadsheet --label pre-v1.4
  update_tracking_sheet.py archive-worksheet --worksheet "Completion Tracker" --label pre-v1.4
  update_tracking_sheet.py upsert-row --worksheet "Completion Tracker" --key-column Issue --key-value 473 --set Status=Done
  update_tracking_sheet.py append-row --worksheet "Completion Tracker" --row-json '["473","Done"]'

Credentials are discovered from GOOGLE_SHEETS_ACCESS_TOKEN,
GOOGLE_APPLICATION_CREDENTIALS, or an authenticated gcloud session.
"""

from __future__ import annotations

import argparse
from datetime import date
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


SHEETS_SCOPE = "https://www.googleapis.com/auth/spreadsheets"
DRIVE_SCOPE = "https://www.googleapis.com/auth/drive"
API_ROOT = "https://sheets.googleapis.com/v4/spreadsheets"
DRIVE_API_ROOT = "https://www.googleapis.com/drive/v3/files"
DEFAULT_SPREADSHEET_ID = "1jiDhstMzCUkke72ePHdmQuIbpZAIlR25JMRB6JuDiE8"
DEFAULT_SPREADSHEET_NAME = "MAP Dev Tracking"
DEFAULT_CREDENTIALS_PATH = os.path.expanduser("~/.config/map-dev-tracking/service-account.json")


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def spreadsheet_id(args: argparse.Namespace) -> str:
    value = args.spreadsheet_id or os.environ.get("MAP_DEV_TRACKING_SPREADSHEET_ID") or DEFAULT_SPREADSHEET_ID
    if not value:
        die("set MAP_DEV_TRACKING_SPREADSHEET_ID or pass --spreadsheet-id")
    if "/spreadsheets/d/" in value:
        parts = value.split("/spreadsheets/d/", 1)[1].split("/", 1)
        return parts[0]
    return value


def load_json_arg(value: str) -> Any:
    if value.startswith("@"):
        with open(value[1:], "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.loads(value)


def shell_token(command: list[str]) -> str | None:
    if not shutil.which(command[0]):
        return None
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    token = result.stdout.strip()
    return token or None


def access_token() -> str:
    token = os.environ.get("GOOGLE_SHEETS_ACCESS_TOKEN")
    if token:
        return token

    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path and os.path.exists(DEFAULT_CREDENTIALS_PATH):
        credentials_path = DEFAULT_CREDENTIALS_PATH
    if credentials_path:
        try:
            from google.auth.transport.requests import Request
            from google.oauth2 import service_account
        except ModuleNotFoundError:
            die(
                "GOOGLE_APPLICATION_CREDENTIALS is set, but google-auth is not installed. "
                "Install google-auth requests, or set GOOGLE_SHEETS_ACCESS_TOKEN."
            )

        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=[SHEETS_SCOPE, DRIVE_SCOPE],
        )
        credentials.refresh(Request())
        if not credentials.token:
            die("service account authentication did not return an access token")
        return credentials.token

    for command in (
        ["gcloud", "auth", "print-access-token"],
        ["gcloud", "auth", "application-default", "print-access-token"],
    ):
        token = shell_token(command)
        if token:
            return token

    die(
        "no Google Sheets credentials found. Set GOOGLE_SHEETS_ACCESS_TOKEN, "
        "GOOGLE_APPLICATION_CREDENTIALS, or authenticate gcloud."
    )


def api_request(
    args: argparse.Namespace,
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
    query: dict[str, str] | None = None,
) -> dict[str, Any]:
    encoded_query = urllib.parse.urlencode(query or {})
    url = f"{API_ROOT}/{spreadsheet_id(args)}{path}"
    if encoded_query:
        url = f"{url}?{encoded_query}"

    data = None
    headers = {"Authorization": f"Bearer {access_token()}"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        payload = error.read().decode("utf-8", errors="replace")
        die(f"Google Sheets API returned {error.code}: {payload}")
    except urllib.error.URLError as error:
        die(f"could not reach Google Sheets API: {error}")

    if not payload:
        return {}
    return json.loads(payload)


def drive_request(
    args: argparse.Namespace,
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
    query: dict[str, str] | None = None,
) -> dict[str, Any]:
    encoded_query = urllib.parse.urlencode(query or {})
    url = f"{DRIVE_API_ROOT}/{path}"
    if encoded_query:
        url = f"{url}?{encoded_query}"

    data = None
    headers = {"Authorization": f"Bearer {access_token()}"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        payload = error.read().decode("utf-8", errors="replace")
        die(f"Google Drive API returned {error.code}: {payload}")
    except urllib.error.URLError as error:
        die(f"could not reach Google Drive API: {error}")

    if not payload:
        return {}
    return json.loads(payload)


def quote_range(a1_range: str) -> str:
    return urllib.parse.quote(a1_range, safe="")


def sheet_a1(worksheet: str, cells: str = "A1") -> str:
    escaped = worksheet.replace("'", "''")
    return f"'{escaped}'!{cells}"


def column_letter(index: int) -> str:
    if index < 0:
        die("column index must be non-negative")
    result = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def normalize_values_matrix(values: Any) -> list[list[Any]]:
    if not isinstance(values, list) or not all(isinstance(row, list) for row in values):
        die("--values-json must be a JSON array of row arrays")
    return values


def parse_sets(values: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for item in values:
        if "=" not in item:
            die(f"--set must be Header=Value, got {item!r}")
        key, value = item.split("=", 1)
        if not key:
            die(f"--set has an empty header name: {item!r}")
        parsed[key] = value
    return parsed


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def archive_label(args: argparse.Namespace) -> str:
    parts = [args.date or date.today().isoformat()]
    if getattr(args, "label", None):
        parts.append(args.label)
    return " ".join(parts)


def default_copy_name(args: argparse.Namespace) -> str:
    if args.copy_name:
        return args.copy_name
    return f"{DEFAULT_SPREADSHEET_NAME} archive {archive_label(args)}"


def safe_worksheet_title(title: str) -> str:
    for character in r"[]:*?/\\":
        title = title.replace(character, "-")
    return title[:100]


def unique_worksheet_title(existing_titles: set[str], desired_title: str) -> str:
    desired_title = safe_worksheet_title(desired_title)
    if desired_title not in existing_titles:
        return desired_title

    for index in range(2, 1000):
        suffix = f" {index}"
        candidate = f"{desired_title[:100 - len(suffix)]}{suffix}"
        if candidate not in existing_titles:
            return candidate
    die(f"could not find a unique worksheet title for {desired_title!r}")


def sheets_metadata(args: argparse.Namespace) -> list[dict[str, Any]]:
    data = api_request(
        args,
        "GET",
        "",
        query={"fields": "sheets(properties(sheetId,title,index,hidden,gridProperties(rowCount,columnCount)))"},
    )
    return [sheet["properties"] for sheet in data.get("sheets", [])]


def worksheet_property(args: argparse.Namespace, title: str) -> dict[str, Any]:
    for sheet in sheets_metadata(args):
        if sheet.get("title") == title:
            return sheet
    die(f"worksheet {title!r} not found")


def run_list_worksheets(args: argparse.Namespace) -> None:
    print_json(sheets_metadata(args))


def run_copy_spreadsheet(args: argparse.Namespace) -> None:
    source_id = spreadsheet_id(args)
    copy_name = default_copy_name(args)
    if args.dry_run:
        print_json(
            {
                "action": "copy-spreadsheet",
                "sourceSpreadsheetId": source_id,
                "copyName": copy_name,
                "sameFolder": not args.no_same_folder,
            }
        )
        return

    body: dict[str, Any] = {"name": copy_name}
    if not args.no_same_folder:
        source = drive_request(
            args,
            "GET",
            urllib.parse.quote(source_id, safe=""),
            query={"fields": "id,name,parents"},
        )
        parents = source.get("parents", [])
        if parents:
            body["parents"] = parents

    data = drive_request(
        args,
        "POST",
        f"{urllib.parse.quote(source_id, safe='')}/copy",
        body=body,
        query={"fields": "id,name,webViewLink"},
    )
    print_json(data)


def run_archive_worksheet(args: argparse.Namespace) -> None:
    source = worksheet_property(args, args.worksheet)
    existing_titles = {sheet["title"] for sheet in sheets_metadata(args)}
    desired_title = args.archive_name or f"{args.worksheet} archive {archive_label(args)}"
    archive_name = unique_worksheet_title(existing_titles, desired_title)
    request = {
        "duplicateSheet": {
            "sourceSheetId": source["sheetId"],
            "insertSheetIndex": source.get("index", 0) + 1,
            "newSheetName": archive_name,
        }
    }
    if args.dry_run:
        print_json({"action": "archive-worksheet", "worksheet": args.worksheet, "request": request})
        return
    data = api_request(args, "POST", ":batchUpdate", body={"requests": [request]})
    print_json({"archiveName": archive_name, "response": data})


def run_reorder_worksheets(args: argparse.Namespace) -> None:
    sheets = sheets_metadata(args)
    by_title = {sheet["title"]: sheet for sheet in sheets}
    missing = [title for title in args.worksheets if title not in by_title]
    if missing:
        die(f"worksheet(s) not found: {', '.join(missing)}")

    requests = [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": by_title[title]["sheetId"],
                    "index": 0,
                },
                "fields": "index",
            }
        }
        for title in reversed(args.worksheets)
    ]
    if args.dry_run:
        print_json({"action": "reorder-worksheets", "frontWorksheets": args.worksheets, "requests": requests})
        return

    data = api_request(args, "POST", ":batchUpdate", body={"requests": requests})
    print_json({"frontWorksheets": args.worksheets, "response": data})


def run_get(args: argparse.Namespace) -> None:
    path = f"/values/{quote_range(args.range)}"
    data = api_request(args, "GET", path)
    print_json(data.get("values", []))


def run_update_range(args: argparse.Namespace) -> None:
    values = normalize_values_matrix(load_json_arg(args.values_json))
    body = {"range": args.range, "majorDimension": "ROWS", "values": values}
    if args.dry_run:
        print_json({"action": "update-range", "range": args.range, "body": body})
        return
    path = f"/values/{quote_range(args.range)}"
    data = api_request(
        args,
        "PUT",
        path,
        body=body,
        query={"valueInputOption": args.value_input_option},
    )
    print_json(data)


def run_append_row(args: argparse.Namespace) -> None:
    row = load_json_arg(args.row_json)
    if not isinstance(row, list) or any(isinstance(cell, list) for cell in row):
        die("--row-json must be a JSON array representing one row")
    body = {"majorDimension": "ROWS", "values": [row]}
    target_range = sheet_a1(args.worksheet)
    if args.dry_run:
        print_json({"action": "append-row", "range": target_range, "body": body})
        return
    path = f"/values/{quote_range(target_range)}:append"
    data = api_request(
        args,
        "POST",
        path,
        body=body,
        query={
            "valueInputOption": args.value_input_option,
            "insertDataOption": "INSERT_ROWS",
        },
    )
    print_json(data)


def run_upsert_row(args: argparse.Namespace) -> None:
    updates = parse_sets(args.set_values)
    read_range = sheet_a1(args.worksheet, args.scan_range)
    rows = api_request(args, "GET", f"/values/{quote_range(read_range)}").get("values", [])
    if not rows:
        die(f"no header row found in {read_range}")

    headers = [str(value) for value in rows[0]]
    header_index = {header: index for index, header in enumerate(headers)}
    missing = [name for name in [args.key_column, *updates.keys()] if name not in header_index]
    if missing:
        die(f"missing header(s): {', '.join(missing)}. Available headers: {', '.join(headers)}")

    key_index = header_index[args.key_column]
    target_row_index = None
    for row_index, row in enumerate(rows[1:], start=2):
        value = row[key_index] if key_index < len(row) else ""
        if str(value) == args.key_value:
            target_row_index = row_index
            break

    row = [""] * len(headers)
    row[key_index] = args.key_value
    if target_row_index is not None:
        existing = rows[target_row_index - 1]
        row[: len(existing)] = existing

    for header, value in updates.items():
        row[header_index[header]] = value

    if target_row_index is None:
        if args.no_append_if_missing:
            die(f"no row found where {args.key_column}={args.key_value}")
        body = {"majorDimension": "ROWS", "values": [row]}
        target_range = sheet_a1(args.worksheet)
        if args.dry_run:
            print_json({"action": "append-row", "range": target_range, "row": row})
            return
        data = api_request(
            args,
            "POST",
            f"/values/{quote_range(target_range)}:append",
            body=body,
            query={
                "valueInputOption": args.value_input_option,
                "insertDataOption": "INSERT_ROWS",
            },
        )
        print_json(data)
        return

    last_column = column_letter(len(headers) - 1)
    target_range = sheet_a1(args.worksheet, f"A{target_row_index}:{last_column}{target_row_index}")
    body = {"range": target_range, "majorDimension": "ROWS", "values": [row]}
    if args.dry_run:
        print_json({"action": "update-row", "range": target_range, "row": row})
        return
    data = api_request(
        args,
        "PUT",
        f"/values/{quote_range(target_range)}",
        body=body,
        query={"valueInputOption": args.value_input_option},
    )
    print_json(data)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spreadsheet-id", help="Spreadsheet ID or full Google Sheets URL")
    parser.add_argument("--dry-run", action="store_true", help="Print the planned write instead of writing")
    parser.add_argument(
        "--value-input-option",
        default="USER_ENTERED",
        choices=["RAW", "USER_ENTERED"],
        help="How Google Sheets should interpret written values",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-worksheets", help="List worksheet metadata")
    list_parser.set_defaults(func=run_list_worksheets)

    copy_parser = subparsers.add_parser("copy-spreadsheet", help="Copy the whole spreadsheet as a release archive")
    copy_parser.add_argument("--copy-name", help="Exact name for the copied spreadsheet")
    copy_parser.add_argument("--label", help="Release or archive label, such as pre-v1.4")
    copy_parser.add_argument("--date", help="Archive date, defaults to today")
    copy_parser.add_argument("--no-same-folder", action="store_true", help="Do not try to create the copy in the source file folder")
    copy_parser.set_defaults(func=run_copy_spreadsheet)

    archive_parser = subparsers.add_parser("archive-worksheet", help="Duplicate a worksheet inside the spreadsheet")
    archive_parser.add_argument("--worksheet", required=True, help="Worksheet/tab name to duplicate")
    archive_parser.add_argument("--archive-name", help="Exact title for the duplicate worksheet")
    archive_parser.add_argument("--label", help="Release or archive label, such as pre-v1.4")
    archive_parser.add_argument("--date", help="Archive date, defaults to today")
    archive_parser.set_defaults(func=run_archive_worksheet)

    reorder_parser = subparsers.add_parser("reorder-worksheets", help="Move named worksheets to the front in the given order")
    reorder_parser.add_argument(
        "--worksheet",
        dest="worksheets",
        action="append",
        required=True,
        help="Worksheet/tab name. Repeat in desired front-tab order.",
    )
    reorder_parser.set_defaults(func=run_reorder_worksheets)

    get_parser = subparsers.add_parser("get", help="Read an A1 range")
    get_parser.add_argument("--range", required=True, help="A1 range, including worksheet name")
    get_parser.set_defaults(func=run_get)

    update_parser = subparsers.add_parser("update-range", help="Update an exact A1 range")
    update_parser.add_argument("--range", required=True, help="A1 range, including worksheet name")
    update_parser.add_argument("--values-json", required=True, help="JSON row matrix or @path to JSON")
    update_parser.set_defaults(func=run_update_range)

    append_parser = subparsers.add_parser("append-row", help="Append a single row to a worksheet")
    append_parser.add_argument("--worksheet", required=True, help="Worksheet/tab name")
    append_parser.add_argument("--row-json", required=True, help="JSON row array or @path to JSON")
    append_parser.set_defaults(func=run_append_row)

    upsert_parser = subparsers.add_parser("upsert-row", help="Update or append a row by matching a key column")
    upsert_parser.add_argument("--worksheet", required=True, help="Worksheet/tab name")
    upsert_parser.add_argument("--scan-range", default="A1:ZZ", help="A1 cells to scan for headers and rows")
    upsert_parser.add_argument("--key-column", required=True, help="Header name used to identify the row")
    upsert_parser.add_argument("--key-value", required=True, help="Cell value to match in the key column")
    upsert_parser.add_argument("--set", dest="set_values", action="append", default=[], required=True, help="Header=Value update")
    upsert_parser.add_argument("--no-append-if-missing", action="store_true", help="Fail if the key row does not exist")
    upsert_parser.set_defaults(func=run_upsert_row)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
