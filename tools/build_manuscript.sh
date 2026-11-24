#!/bin/bash
# Two-pass build: render to PDF to find the page of each section, then rebuild with page numbers in Contents.
set -e
cd "$(dirname "$0")/.."
S=${DOCX_SKILL:-/root/.claude/skills/synced/981ad0bf-8e9b-49c6-ba4a-5c7632818e0a_13758d69-edb2-46df-8859-79b35df62f91/docx}
TMP=$(mktemp -d)
DOCX=manuscript/The_Complete_Amish_Dry_Mix_Pantry_Cookbook_Manuscript.docx
for pass in 1 2; do
  node tools/build_manuscript.js
  zip -d "$DOCX" '*/' >/dev/null 2>&1 || true
  python3 "$S/scripts/office/soffice.py" --headless --convert-to pdf --outdir "$TMP" "$DOCX" >/dev/null 2>&1
  python3 - "$TMP"/*.pdf <<'PY'
import json, subprocess, sys
pdf = sys.argv[1]
titles = json.load(open('manuscript/.toc.json'))
n = int([l for l in subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout.splitlines() if l.startswith('Pages')][0].split()[1])
pages = {}
for i in range(4, n + 1):  # skip title, copyright, contents
    first = subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout.strip().split('\n')
    head = ' '.join(first[:2])
    for t in titles:
        if t not in pages and (head.startswith(t) or first[0].strip() == t):
            pages[t] = i
missing = [t for t in titles if t not in pages]
if missing: print('pages not found for', missing)
json.dump(pages, open('manuscript/.pages.json', 'w'))
print('pages:', n)
PY
done
cp "$TMP"/*.pdf manuscript/preview.pdf
rm -rf "$TMP"
