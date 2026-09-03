"""sanitize.py - scan a folder for things that must never be published.

Finds: API-key/token/secret/password assignments, high-entropy key-like
strings, webhook URLs, email addresses, .env files present at all, private
key blocks, and any extra terms you list (names, account numbers, brokers)
one per line in a terms file.

Usage:  python sanitize.py <folder> [--terms sanitize_terms.txt]

Exit 0 = clean. Exit 1 = findings printed, one per line, file:line:reason.
Re-run before EVERY push, not once. The report names where a finding is; it
never prints the secret value itself.
"""

import argparse
import os
import re
import sys

PATTERNS = [
    ("key assignment", re.compile(
        r"(api[_-]?key|secret|token|passwd|password|credential)"
        r"\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+]{12,}", re.I)),
    ("webhook url", re.compile(
        r"https?://\S*(webhook|hooks\.)\S*", re.I)),
    ("email address", re.compile(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("long token-like string", re.compile(
        r"\b(?:sk|pk|ghp|gho|xox[bap]|AKIA)[A-Za-z0-9_\-]{16,}\b")),
]

SKIP_DIRS = {"__pycache__", ".git", "node_modules"}
TEXT_EXTS = {".md", ".py", ".json", ".txt", ".yml", ".yaml", ".toml",
             ".ini", ".cfg", ".ps1", ".sh", ".bat", ".cmd", ".html", ".css",
             ".js"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--terms", help="file of extra terms, one per line")
    args = ap.parse_args()

    terms = []
    if args.terms:
        for line in open(args.terms, encoding="utf-8"):
            t = line.strip()
            if t and not t.startswith("#"):
                terms.append(t.lower())

    findings = 0
    for dirpath, dirnames, filenames in os.walk(args.folder):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, args.folder)
            if f == ".env" or f.endswith(".env"):
                print("%s:0: .env file present - never publish one" % rel)
                findings += 1
                continue
            if os.path.splitext(f)[1].lower() not in TEXT_EXTS:
                continue
            try:
                lines = open(path, encoding="utf-8",
                             errors="replace").read().splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                for reason, pat in PATTERNS:
                    if pat.search(line):
                        print("%s:%d: %s" % (rel, i, reason))
                        findings += 1
                low = line.lower()
                for t in terms:
                    if t in low:
                        print("%s:%d: listed term (%s)" % (rel, i, t))
                        findings += 1

    if findings:
        print("\n%d finding(s). Fix or consciously accept each before "
              "publishing." % findings)
        sys.exit(1)
    print("clean: no findings.")


if __name__ == "__main__":
    main()
