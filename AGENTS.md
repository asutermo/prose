# Guide for agents

This repo is one agent skill, `prose`. `SKILL.md` at the root is the skill. Pass 1 lists the 31 AI tells in a table (§1 to §26 in the order of blader/humanizer, §27 to §31 from its patterns 30-34). Pass 2 lists the STE80 structure rules (S1 to S15). Part 2 lists the bulk-text principles, Part 3 the PR template, Part 4 the user-facing docs rules. Follow these rules when you change it.

- **Write in the style the skill teaches.** Short sentences, active voice, simple tenses, one term per thing.
- **Keep the release version in sync** in `SKILL.md` (`metadata.version`) and the latest release heading in `CHANGELOG.md`. This repo does not ship plugin manifests.
- **Keep SKILL.md under 500 lines** (Anthropic's limit) and about 3,000 words. SKILL.md holds compact tables. Full entries, long examples and anything for human readers go in `references/` or the README.
- **Keep the entry format in `references/ai-tells.md`:** Watch for, Problem, Before, After.
- **Keep LICENSE a plain MIT license.** Keep the blader/humanizer MIT notice in `THIRD_PARTY_NOTICES.md` as long as Pass 1 follows its catalog.
- **Keep SKILL.md and README.md in sync** when you add, remove or rename a tell or a rule. Part 2 (bulk text) and Part 3 (PR/commit text) are part of the skill; keep their summaries in the README in sync too. Keep `references/ste80-rules.md` mapped to the S-rules.
- **Keep `scripts/ste_check.py` in sync** with the tells and words in SKILL.md where a regex can find them.
- **Do not copy the ASD-STE100 specification or dictionary.** ASD owns the copyright. Paraphrase rules in your own words. Cite only single word pairs.
- **Do not claim compliance.** The skill and the checker give "STE style", not certified STE.
## Safety and guardrails

- **Never commit credentials, tokens, private URLs, private repo names, account data, or capture artifacts.** Run `python scripts/check_prose.py` before any authorized commit. It scans text files, including its own source, and skips binary assets and the ignored private blocklist. Private-content checking needs `scripts/private-blocklist.local`; a missing blocklist produces a warning.
- **Never commit local operating notes.** Notes taken while applying the skill to private repos stay in private infrastructure (this bit once: an operational notes file rode into the first push and had to be purged from history with a commit-tree rewrite).
- **History rewrites on MSYS git:** `filter-branch` fails here. Use the commit-tree loop (read-tree, rm --cached, write-tree, preserve GIT_AUTHOR_* / GIT_COMMITTER_* from each source commit, commit-tree, update-ref). Never leave a `commit-tree` without `-m` (it hangs on stdin).

## Before you publish

```bash
python scripts/ste_check.py --help
python scripts/check_prose.py
python -m unittest discover -s tests -v
npx skills add . --list
```

## Keeping the installed skill in sync

This repo is published at github.com/asutermo/prose. Local edits do not authorize commits, pushes or changes to installed skills. Stop at the diff when the user requests review first. After the user authorizes publication and installation:

1. Edit in this repo, run the publish checks above, commit.
2. Push to GitHub (the origin remote; plain `git push`).
3. Copy the files listed in `SYNC_PAIRS` in `scripts/check_prose.py` into the selected installed skill directory. Never copy `scripts/private-blocklist.local`.
4. Verify with `python scripts/check_prose.py --sync`, which diffs the tracked sync pairs against the installed copy and reports any drift.
