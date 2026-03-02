"""Fetch all records from Cambridge data API and print dataset names alphabetically."""

from __future__ import annotations

import json
import sys
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

API_URL = "https://data.cambridgema.gov/resource/3gki-wyrb.json"
PAGE_SIZE = 2000


def fetch_all_records(url: str, page_size: int = PAGE_SIZE) -> list[dict]:
	"""Fetch every record from a Socrata endpoint using offset pagination."""
	offset = 0
	all_records: list[dict] = []

	while True:
		query = urlencode({"$limit": page_size, "$offset": offset})
		request_url = f"{url}?{query}"
		with urlopen(request_url, timeout=30) as response:
			page = json.load(response)

		if not page:
			break

		all_records.extend(page)

		if len(page) < page_size:
			break

		offset += page_size

	return all_records


def extract_dataset_names(records: Iterable[dict]) -> list[str]:
	"""Extract unique dataset-like names and return them sorted alphabetically."""
	preferred_fields = ("dataset", "dataset_name", "name", "type", "subtype")
	names: set[str] = set()

	for record in records:
		for field in preferred_fields:
			value = record.get(field)
			if isinstance(value, str) and value.strip():
				names.add(value.strip())
				break

	return sorted(names, key=str.casefold)


def main() -> int:
	try:
		records = fetch_all_records(API_URL)
		dataset_names = extract_dataset_names(records)
	except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
		print(f"Failed to fetch records: {exc}", file=sys.stderr)
		return 1

	if not dataset_names:
		print("No dataset names were found in the records.")
		return 0

	for name in dataset_names:
		print(name)

	return 0


#if __name__ == "__main__":
	#raise SystemExit(main())
main()