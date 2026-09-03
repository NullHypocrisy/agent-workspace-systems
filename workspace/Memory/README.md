# The Memory System

Any assistant memory has to solve three problems: getting facts written
down (**store**), choosing what a fresh session reads before it starts
(**inject**), and finding an old fact again with a traceable source
(**recall**). This system solves them with plain files plus one small
SQLite index — no service, no API, no vendor.

## The three tiers

**Core profile** (`global/core-profile.md`) — the slim, always-loaded
identity file: who the user is, how they want to be worked with. Stable
facts only; nothing volatile.

**Working memory** — one small capped file per tenant holding the standing
present: only what is true NOW and has no other home. The admission test and
write protocol live in `AGENTS.md` at the workspace root. Caps live in
`tenants.json`; a file under sustained cap pressure has lines that belong in
other files, and the fix is re-homing them, not raising the cap.

**Day logs** (`<tenant>/logs/YYYY-MM-DD.md`) — pure archive, one entry per
session per tenant touched, written at session close. Never loaded at
session start; recall reaches them, and there a dated entry is doing a
record's proper job — claiming only what held on its own date.

## Tenants

A tenant is a topic or project with its own working memory and logs.
`tenants.json` is the registry: each tenant names its folder, its cap, and
the file globs (`scopes`) the indexer should include for it. Two kinds:

- A **project tenant** also has live documents of its own elsewhere in the
  workspace; add those folders to its scopes so recall covers them.
- A **bucket tenant** is a life-topic archive (health, home, hobbies...)
  that exists only for recall — nothing loads it unless the conversation
  enters its territory.

The starter registry ships with `global` plus one `example-project` tenant.
Add tenants by copying the pattern; the engine is generic over the registry
and needs no code change.

## The engine

Three scripts in `engine/`, standard library only:

- `indexer.py` — walks every tenant's scopes, splits markdown files into
  chunks by heading, and stores them in `index/memory.db` with SQLite FTS5
  full-text search. Incremental: unchanged files (by content hash) are
  skipped. Rerun it nightly or whenever you want fresh recall. Secrets are
  excluded unconditionally: `.env` files and anything matching key-like
  patterns are never indexed, whatever the scopes say.
- `search.py` — keyword recall over the index:
  `python engine/search.py "query" [--tenant NAME] [--limit N]`.
  Every hit prints its source file, heading, and file date — a citation, so
  the answer can be traced. No hits means "not found in memory", said
  plainly.
- `evict.py` — the safe way to remove a line from a working-memory file:
  `python engine/evict.py <memory-file> "exact line text"`.
  It appends the line to today's day log for that tenant first, re-reads the
  log to confirm the line landed, and only then removes it. It refuses
  anything it cannot read back, so nothing vanishes silently.

## What keeps this honest

- Every line in memory traces to a source; recall always cites.
- Store is curated by the assistant at session close, against the admission
  test — not an automatic transcript dump. Day logs may carry summaries,
  but only of what actually happened, written by the session that did it.
- The index is derived and disposable: delete `index/memory.db` and rerun
  the indexer to rebuild it from the files, which are the truth.
