# Cambridge Open Data Archiving Audit

A small Python utility that finds datasets on `data.cambridgema.gov` that are **not enrolled in archiving** using the Socrata Discovery API.

## Project Name Suggestion

Use this repository name on GitHub:
`cambridge-open-data-archiving-audit`

## What It Does

- Calls `https://data.cambridgema.gov/api/catalog/v1`
- Filters with `enrolled_in_archival=false`
- Paginates through all results
- Prints unique dataset links in alphabetical order
- Optionally writes links to an output file

## Files

- `cambridge_archiving_audit.py`: Main script
- `not-enrolled-in-archiving.py`: Backward-compatible wrapper
- `get-police-data.py`: Earlier API test script

## Run

```powershell
& ".\.venv\Scripts\python.exe" cambridge_archiving_audit.py
```

Write output to a file:

```powershell
& ".\.venv\Scripts\python.exe" cambridge_archiving_audit.py --output links.txt
```

## Push to GitHub

```powershell
git init
git add .
git commit -m "Initial commit: archiving audit script"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```
