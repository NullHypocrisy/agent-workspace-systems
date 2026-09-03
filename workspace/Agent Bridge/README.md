# The Agent Bridge

File-based messaging between projects (or agents) that are deliberately
walled off from each other. Walls are good — one project's assistant should
not edit another's files — but they need one sanctioned channel across.
This folder is it: the single location where every project has both read
and write access, and the only one outside a project's own tree.

## Filing a message

    Agent Bridge/to-<realm>/FROM-<sender>_<date>_<slug>.md

Each `to-<realm>` folder belongs to the project expected to act on what
lands in it. The starter installation ships `to-global/`; create one folder
per project or agent you add. Because sender and date are in the filename,
listing an inbox is enough to see its traffic at a glance.

A message starts with a fenced frontmatter block — see
`templates/message-template.md`. The `kind` field tells the reader what is
being asked:

- **work** — a complete specification for something to build, written so it
  can be handed to a session with no other context.
- **finding** — knowledge worth passing along; nothing is asked of the
  reader.
- **question** — asks for an answer, which arrives as a `reply` filed to
  the asker's inbox.
- **reply** — answers an earlier message, named in its `reply-to` field.

## Delivery

An inbox is only delivered if something reads it. Give each active inbox a
reader — a scheduled session, or a standing instruction in that project's
rules to check its inbox at session start. A message filed to an inbox with
no reader is undelivered mail: the session that files one must say so to the
user in plain words, naming the file and what waits.

## Three rules

- **The sender never acts on the other side of the wall.** A message is a
  request or a report, never a substitute for the receiving project doing
  the work itself.
- **Close by editing `status`, never by deleting.** Set it to `done` or
  `answered` and keep the file: the history of cross-project requests is
  worth more than an empty folder.
- **Archive closed messages** into `to-<realm>/closed/`, moved by the
  session that actioned them, filename unchanged. A stale reference to a
  bridge message then resolves deterministically: insert `closed/` between
  inbox and filename.
