# Quarantine, Cleanup & Backup

The hygiene layer. Its principle: **nothing is ever hard-deleted in the
moment.** Files retire through a cooling-off pipeline, and deletion happens
only after an expiry has passed, nothing load-bearing still references the
file, and a backup already holds a copy.

## The pipeline

1. A session retires a file: move it to `Quarantine/` (mirroring its
   original relative path) and append one manifest line. Throwaway scratch
   skips the move — it is born in `Temp/managed/` with an expiry.
2. `backup.py` snapshots the whole workspace to dated folders on whatever
   destinations `workspace.json` names — a daily tier and a weekly tier,
   each keeping N dated folders. Retention counts folders BY NAME, never by
   filesystem timestamp (timestamps do not survive drive moves). SQLite
   databases are snapshotted through the sqlite backup API, never raw-copied
   while possibly write-active. The backup reads the workspace and writes
   out; it never writes back.
3. `cleanup.py` runs weekly, after the weekly backup. For each file in
   `Quarantine/` and `Temp/managed/` it asks: past expiry? unreferenced by
   any load-bearing surface (scripts, config, skills, open specs — not by
   logs or archives, which mention retired files precisely because they were
   retired)? and did this week's backup land (if backups are configured)?
   Only a yes to all three deletes. Everything else is held and reported.
   Nothing outside those two folders is ever deleted — the boundary is
   enforced in code, not convention.

## Running

    python Maintenance/backup.py --tier daily     (mornings)
    python Maintenance/backup.py --tier weekly    (Sunday, before cleanup)
    python Maintenance/cleanup.py                 (Sunday, after backup)
    python Maintenance/cleanup.py --dry-run       (see what would happen)

Each run appends one outcome line to its log beside the script, even on a
crash. Set destinations in `workspace.json` before the first backup; with
none set, backup.py reports and exits, and cleanup.py (with
`require_backup` true) refuses to delete.

`smoke_test.py` exercises all four systems end to end in a throwaway copy
and prints PASS/FAIL per system. Run it after install and after any edit to
the machinery.
