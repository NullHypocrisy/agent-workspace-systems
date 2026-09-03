# Managed temp manifest

`Temp/managed/` is self-clearing scratch: anything written here carries an
expiry from birth, so "delete after use" stops depending on a session
remembering. One line per file:

    date_in | expiry | filename | reason

A file with no line expires the cooling window (workspace.json) after its
own filesystem age. The weekly cleanup removes what is past expiry.

---
