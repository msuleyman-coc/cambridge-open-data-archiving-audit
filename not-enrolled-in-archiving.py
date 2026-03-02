"""Backward-compatible wrapper for the renamed script.

Use `cambridge_archiving_audit.py` as the primary script.
"""

from cambridge_archiving_audit import main


if __name__ == "__main__":
    raise SystemExit(main())
