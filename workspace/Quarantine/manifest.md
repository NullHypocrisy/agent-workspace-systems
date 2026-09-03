# Quarantine manifest

Moving a file into `Quarantine/` means also appending ONE line to this file
in the same session. Inside `Quarantine/` the file sits at the same relative
path it had in the workspace, so restoring it is a move back plus deleting
its line here.

One pipe-delimited line per file; make single-line edits only, and never
regenerate or rewrite the whole file:

    date_in | expiry | original_path | reason

A line's expiry defaults to its date_in plus the cooling window set in
workspace.json (14 days). The weekly cleanup (`Maintenance/cleanup.py`)
discovers files by walking the folder itself, consulting this manifest only
for recorded expiries. A file past expiry is removed only after a fresh
search shows no load-bearing surface still references it — and this
manifest is never touched by the deleter, so the line for a removed file
remains as the permanent record that it existed.

---
