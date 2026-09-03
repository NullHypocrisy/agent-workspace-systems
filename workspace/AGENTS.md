# Workspace rules — read at the start of every session

You are an AI assistant operating in this workspace. These rules bind every
session. Each subsystem's own README carries its full design; this file
carries only what must be true everywhere.

## Truth

Live checks beat written records, and written records beat anything
remembered or assumed. A file, an index, or a prior session's claim is a
claim, not a fact: when the real state is checkable, check it before
asserting it or acting on it. Prefer writing down how to get an answer (a
query, a path, a dated observation) over writing down a frozen answer.
Anything you cannot verify, call unverifiable — never guess. A dated line in
a log claims truth as of its date, and that is legitimate.

## Record once

Every fact has exactly one authoritative home. Everything else points at
that home or is generated from it by a script that can be rerun. Never
hand-copy a fact into a second file — a paraphrase counts as a copy. When
two files disagree, that is a defect to surface and fix immediately, never
to read past. When something changes state, move it to its new home; do not
leave it in both.

## Session start

Read, in order:
1. This file.
2. `Memory/global/working-memory.md` and `Memory/global/core-profile.md`.
3. The working memory of the project the session belongs to, if it has one
   (`Memory/<project>/working-memory.md`).
4. `Work Items/00_index.md` — the open-work view.

Day logs are archive: never read them at session start; reach them through
search (`Memory/engine/search.py`) when history is needed.

## Session close

Before ending, write the close artifacts:
1. One day-log entry per project the session touched:
   `Memory/<project>/logs/YYYY-MM-DD.md` (or `Memory/global/logs/` for
   sessions belonging to no project). Append; fold your own corrections in
   before writing rather than appending contradictions after.
2. Working-memory updates, per the admission test below.
3. If a work item was created or completed, the Work Items README's
   lifecycle steps must already have run — they are part of the work, not
   part of the close.

A session survives only as its files: whatever was not written down before
the end is gone.

## Working memory — the admission test

A working-memory file holds the standing present: only what is true NOW and
has no other home. Before adding a line, ask three questions in order:

1. Does this outcome change what is true now? Most output fails here and
   belongs to the day log alone.
2. If so, is there already a file that owns that truth? Finished work is
   owned by its spec, rules by rules files, project facts by the project's
   own documents — update the owner, not memory.
3. Only what survives both questions enters working memory.

Writes are surgical: add lines, or replace a line your own work superseded.
Before deleting or replacing a line an earlier session wrote, copy it into
today's day log (use `Memory/engine/evict.py`, which refuses to remove
anything it cannot read back). Never rewrite a memory file wholesale. Each
file's size cap lives in `Memory/tenants.json`; sustained cap pressure means
lines are homed wrong, not that the cap is too small.

## Work

Work that will not finish in the current session becomes a work item:
follow `Skills/work-item-SKILL.md`. The system itself is described in
`Work Items/README.md`. Never edit generated files (the completed archive);
edit the source and rerun the builder.

## Retiring files

Nothing is hard-deleted. A file that has served its purpose moves to
`Quarantine/` (mirroring its original relative path) with one line appended
to `Quarantine/manifest.md` in the same session. Throwaway scratch is
written to `Temp/managed/` with a manifest line carrying its expiry. The
weekly cleanup (`Maintenance/cleanup.py`) deletes only what is past expiry,
unreferenced by anything load-bearing, and already captured by a backup.

## Messages between projects

Projects do not write into each other's folders. Anything one project needs
to tell another goes through `Agent Bridge/` — see its README for the
message format and the archive convention.

## Dates and secrets

Read the clock before writing any date or time — a session's idea of "today"
goes stale, and file timestamps may be in UTC while the clock is local.
Never print, echo, or log a secret value; secrets live only in `.env` files,
which are read into variables and never displayed. Never index or back up a
secret's value anywhere its content could be searched or shared.
