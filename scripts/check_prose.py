#!/usr/bin/env python3
"""Guardrails for the prose skill repo.

Run before committing or pushing:

    python scripts/check_prose.py            # secrets/PII scan only
    python scripts/check_prose.py --sync     # also diff against the installed Hermes skill copy

Exit code 0 = clean, 1 = findings.

Private content rules live in `scripts/private-blocklist.local`
(untracked, gitignored): one case-insensitive substring per line. This
file never contains the entries themselves, because this file is
published. If the blocklist file is missing, the private-content check
is skipped with a warning; the generic secret scan still runs.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Files that must never be scanned as text
BINARY_EXT = {".png", ".jpg", ".gif", ".zip", ".exe", ".dll", ".pdf"}

# Secret-shaped patterns. These are generic signatures, not private data.
SECRET_PATTERNS = [
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("private-key-block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("bearer-token", re.compile(r"\bbearer\s+[A-Za-z0-9_\-\.]{25,}", re.I)),
    ("generic-assignment", re.compile(r"\b(api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}", re.I)),
]

BLOCKLIST_PATH = os.path.join(REPO, "scripts", "private-blocklist.local")

SYNC_PAIRS = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "THIRD_PARTY_NOTICES.md",
    "PROVENANCE.md",
    "LICENSE",
    "AGENTS.md",
    ".gitignore",
    "agents/openai.yaml",
    "references/ai-tells.md",
    "references/ste80-rules.md",
    "references/word-swaps.md",
    "references/strict-mode.md",
    "references/worked-example.md",
    "references/user-facing-docs.md",
    "scripts/ste_check.py",
    "scripts/check_prose.py",
]


def load_blocklist():
    if not os.path.exists(BLOCKLIST_PATH):
        return None
    entries = []
    with open(BLOCKLIST_PATH, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line and not line.startswith("#"):
                entries.append(line)
    return entries


def iter_files():
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "node_modules"}]
        for name in files:
            path = os.path.join(root, name)
            rel = os.path.relpath(path, REPO).replace("\\", "/")
            yield rel, path


def scan_secrets():
    findings = []
    blocklist = load_blocklist()
    if blocklist is None:
        print("check_prose: WARNING no scripts/private-blocklist.local; private-content check skipped")
    for rel, path in iter_files():
        ext = os.path.splitext(rel)[1].lower()
        if ext in BINARY_EXT:
            continue
        if rel == "scripts/private-blocklist.local":  # the blocklist lists the private strings itself
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                text = handle.read()
        except OSError:
            findings.append(f"{rel}: unable to read")
            continue
        for label, pattern in SECRET_PATTERNS:
            for m in pattern.finditer(text):
                line = text[: m.start()].count("\n") + 1
                findings.append(f"{rel}:{line}  secret-shaped: {label}")
        if blocklist:
            for needle in blocklist:
                for m in re.finditer(re.escape(needle), text, re.I):
                    line = text[: m.start()].count("\n") + 1
                    findings.append(f"{rel}:{line}  forbidden content")
    return findings


def check_sync():
    findings = []
    hermes = os.environ.get("HERMES_SKILLS_DIR")
    if not hermes:
        home = os.path.expanduser("~")
        for cand in (
            os.path.join(home, "AppData", "Local", "hermes", "skills", "prose"),
            os.path.join(home, ".hermes", "skills", "prose"),
            os.path.join(home, ".local", "share", "hermes", "skills", "prose"),
        ):
            if os.path.isdir(cand):
                hermes = cand
                break
    if not hermes:
        findings.append("sync: no installed skill copy found; pass HERMES_SKILLS_DIR to check")
        return findings
    if not os.path.isdir(hermes):
        findings.append("sync: installed skill directory missing")
        return findings
    for rel in SYNC_PAIRS:
        a = os.path.join(REPO, rel)
        b = os.path.join(hermes, rel)
        if not os.path.exists(a):
            findings.append(f"sync: repo file missing: {rel}")
            continue
        if not os.path.exists(b):
            findings.append(f"sync: installed copy missing: {rel}")
            continue
        with open(a, encoding="utf-8", errors="replace") as handle:
            ta = handle.read().replace("\r\n", "\n")
        with open(b, encoding="utf-8", errors="replace") as handle:
            tb = handle.read().replace("\r\n", "\n")
        if ta != tb:
            findings.append(f"sync: differs: {rel}")
    return findings


def main():
    findings = scan_secrets()
    if "--sync" in sys.argv:
        findings += check_sync()
    if findings:
        print(f"check_prose: {len(findings)} finding(s)")
        for f in findings:
            print("  " + f)
        return 1
    print("check_prose: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
