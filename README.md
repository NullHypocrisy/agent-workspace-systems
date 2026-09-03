# Portable Systems — a working memory, work-tracking, messaging and hygiene layer for AI-assisted workspaces

Four systems that make an AI assistant's workspace durable across sessions,
providers, and machines. They were built for daily use in one person's
workspace and rebuilt here as a general, installable set. Nothing in this
folder is a copy of that workspace — every file here is a fresh, portable
version of the mechanics.

The four systems:

1. **Memory** — what the assistant knows between sessions: a small
   always-loaded "working memory" per topic, append-only day logs, and a
   full-text search index so anything ever written down can be found again
   with a citation.
2. **Work Items** — durable task tracking: one spec document per piece of
   work, a one-line-per-item index, and a generated archive of everything
   completed.
3. **Agent Bridge** — file-based messaging between otherwise walled-off
   projects or agents, with inboxes, statuses, and an archive convention.
4. **Quarantine & Backup** — nothing is hard-deleted: retired files cool off
   in a quarantine folder with a manifest and an expiry, a weekly cleanup
   deletes only what is expired, unreferenced, and already backed up, and a
   backup script snapshots the whole workspace to dated folders.

## Requirements

- Python 3.10 or newer, on any OS. Every script is standard library only.
  (Search uses SQLite FTS5, which ships in the standard `sqlite3` builds on
  Windows, macOS, and nearly all Linux distributions.)
- Any AI assistant that can read files in a folder and run shell commands —
  Claude, a local model behind an agent framework, or anything comparable.
  Nothing here calls a model API; the assistant is the operator, the scripts
  are the machinery.

## Install

1. Copy the `workspace/` folder to wherever your assistant works — e.g.
   `~/agent-workspace` or `D:\Workspace`. The folder is the installation;
   there is no installer.
2. Open `workspace.json` and fill in what you want to differ from the
   defaults (backup destinations are the only settings the scripts cannot
   guess).
3. Point your assistant at `AGENTS.md` in the workspace root as the file it
   reads at the start of every session. For Claude-based tools, copy or
   rename it to `CLAUDE.md`; for other tools, use whatever "read this first"
   mechanism they honor (system prompt include, rules file, etc.).
4. Run the smoke test: `python "Maintenance/smoke_test.py"` from the
   workspace root. It exercises the indexer, search, the work-item index
   builder, cleanup (dry run), and backup (dry run), and prints PASS/FAIL
   per system.

Everything works from that point: sessions read `AGENTS.md`, write memory and
day logs, track work items, and the maintenance scripts run whenever you (or
your task scheduler) invoke them.

## Scheduling (optional but recommended)

The maintenance scripts are designed to be run on a schedule, but nothing
breaks if they are not — they can also be run by hand or by the assistant.

- `Maintenance/backup.py --tier daily` — every morning.
- `Maintenance/backup.py --tier weekly` — Sunday morning, before cleanup.
- `Maintenance/cleanup.py` — Sunday evening, after the weekly backup.
- `Memory/engine/indexer.py` — nightly, so each day's writing is searchable
  by morning.

Use Task Scheduler on Windows, cron/launchd elsewhere.

## Layout

    workspace/
      AGENTS.md            <- the rules the assistant reads every session
      workspace.json       <- the one config file (paths, caps, retention)
      Memory/              <- working memory, day logs, search engine
      Work Items/          <- specs, index, completed archive, index builder
      Agent Bridge/        <- cross-project message folders
      Quarantine/          <- cooling-off area for retired files + manifest
      Temp/managed/        <- self-clearing scratch (expiry from birth)
      Maintenance/         <- backup.py, cleanup.py, smoke_test.py
      Skills/              <- procedure files the assistant follows on demand

Each system's folder carries its own README with the full design. `AGENTS.md`
carries only the rules that bind every session; it points at the READMEs
rather than repeating them.

## Sanitizing before you publish or share

`sanitize.py` (beside this README) scans a folder for things that must never
leave a private workspace: API keys and tokens, webhook URLs, email
addresses, password-like assignments, and any extra terms you list (names,
account numbers, broker names) in a `sanitize_terms.txt` file. Run it over
your copy of the set — or over anything else — before pushing to a
repository:

    python sanitize.py <folder> [--terms sanitize_terms.txt]

Exit code 0 means no findings; 1 means findings were printed, one per line
with file and line number. It is re-runnable and should be run before every
push, not once.
