"""List dataset links not enrolled in archiving on data.cambridgema.gov.

Usage:
    python cambridge_archiving_audit.py
    python cambridge_archiving_audit.py --output links.txt
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable
from urllib.parse import urlencode
from urllib.request import urlopen

BASE_URL = "https://data.cambridgema.gov/api/catalog/v1"
PAGE_SIZE = 2000


def fetch_non_archived_datasets(limit: int = PAGE_SIZE) -> list[dict]:
    """Fetch all dataset catalog entries with enrolled_in_archival=false."""
    offset = 0
    all_results: list[dict] = []

    while True:
        params = {
            "enrolled_in_archival": "false",
            "asset_selector": "true",
            "limit": str(limit),
            "offset": str(offset),
            "order": "updatedAt DESC",
            "q": "",
            "search_context": "data.cambridgema.gov",
            "show_unsupported_data_federated_assets": "false",
            "show_visibility": "true",
            "only": "datasets",
        }
        url = f"{BASE_URL}?{urlencode(params)}"

        with urlopen(url, timeout=30) as response:
            page = json.load(response)

        results = page.get("results", [])
        if not results:
            break

        all_results.extend(results)

        if len(results) < limit:
            break

        offset += limit

    return all_results


def build_dataset_links(results: Iterable[dict]) -> list[str]:
    """Build and return unique dataset links, sorted alphabetically."""
    links: set[str] = set()

    for item in results:
        link = item.get("link")
        permalink = item.get("permalink")
        resource = item.get("resource", {})
        dataset_id = resource.get("id")

        if isinstance(link, str) and link.strip():
            links.add(link.strip())
        elif isinstance(permalink, str) and permalink.strip():
            links.add(permalink.strip())
        elif isinstance(dataset_id, str) and dataset_id.strip():
            links.add(f"https://data.cambridgema.gov/d/{dataset_id.strip()}")

    return sorted(links, key=str.casefold)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List links to datasets not enrolled in archiving."
    )
    parser.add_argument(
        "--output",
        help="Optional output file path. If provided, links are written there.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        results = fetch_non_archived_datasets()
        links = build_dataset_links(results)
    except Exception as exc:
        print(f"Failed to fetch discovery API results: {exc}", file=sys.stderr)
        return 1

    if not links:
        print("No datasets found with enrolled_in_archival=false.")
        return 0

    output_text = "\n".join(links)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text + "\n")
        print(f"Wrote {len(links)} link(s) to {args.output}")
    else:
        print(f"Found {len(links)} dataset link(s):")
        print(output_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
