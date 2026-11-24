# Changelog
## 5.2.0

- Added scripts/check_prose.py: a secrets/PII and private-content scanner that must pass before any commit, plus a --sync mode that diffs the repo against the installed Hermes skill copy.
- Added .gitignore (Python artifacts, scratch, editor and OS files, local skill copies).
- AGENTS.md now documents the publish checks and the repo-to-GitHub-to-installed-skill sync workflow.
- Removed references/repo-pass-notes.md, private operational notes that rode into the initial push, and purged it from history with a commit-tree rewrite (filter-branch does not work on MSYS git). Metadata preserved.

## 5.1.1

- Added PROVENANCE.md: a file-by-file breakdown of what is verbatim Dodaios/ste80-humanizer content and what is new in this repo, linked from the top of the README.

## 5.1.0

- New Part 4: user-facing docs rules, adapted from landaire/config. The standing assumption is that a README's reader is a user, not an auditor: tl;dr first, usage before contributor material, common case plus one example, internal detail in a linked developer doc, plain you/we voice.
- The rules live in full in references/user-facing-docs.md, compact in SKILL.md.
- README now states that prose is a standalone skill that started from Dodaios/ste80-humanizer, not a fork.

## 5.0.0

- Renamed the skill to `prose`. It now covers three text surfaces, not one:
  - Pass 1 grew from 26 to 31 AI tells. The new §27 to §31 come from blader/humanizer patterns 30-34: forced metaphors, dramatic fragmentation, rhetorical questions answered immediately, sentence-opener tics, and reassurance kickers. The marketing and blog cliché list moved into SKILL.md.
  - New Part 2: the five readability principles for bulk text (lists, tables, feeds), from Full Stack Data Lab's October 2026 post.
  - New Part 3: the PR body template and commit message rules, adapted from Humanlayer's show-me skill.
- SKILL.md stays under 500 lines (322). The checker flags only protected literals in the new parts.


## 4.0.0

- SKILL.md is now 217 lines instead of 573, and about 2,650 words instead of 6,250. Pass 1 and Pass 2 are compact tables with one example per group.
- The full entries for the 26 AI tells moved to `references/ai-tells.md`. The worked example moved to `references/worked-example.md`.
- AGENTS.md now sets a limit of 500 lines for SKILL.md.

## 3.2.1

- LICENSE is now a plain MIT license. The blader/humanizer MIT notice moved to `THIRD_PARTY_NOTICES.md`.

## 3.2.0

- Cut SKILL.md down to what the model needs. The story of Karpathy's post, the note about the graphic and the sources moved out. They are in the README.
- Fixed a sentence in the README that had an AI tell.

## 3.1.0

- Renamed from `humanizer-ste80` to `ste80-humanizer` ("STE80 Humanizer"). Install with `npx skills add Dodaios/ste80-humanizer`. The slash command is now `/ste80-humanizer`.

## 3.0.0

- Rewrote SKILL.md from top to bottom for readability.
- New section "How to read this skill": two passes, §1 to §26 for AI tells, S1 to S15 for structure, the same fields in every entry.
- New section "The method": Karpathy's full tip, the ladder from writing to diagrams, HTML and video, why STE works on LLMs, a table of what 100% and 80% mean, and a note on errors in the graphic that came with his post.
- Pass 1 now covers all 26 patterns of blader/humanizer in the same order (adds hyphenated pairs, vague association, repeated heading, borrowed authority with prestige lists, and others), each with Watch for, Problem, and new Before/After examples. The MIT notice of blader/humanizer is in LICENSE.
- Pass 2 has 15 S-rules, each with 80% and Strict levels and examples.
- New worked example that shows the text after Pass 1 and after Pass 2.
- Return formats now include file mode, embedded mode and review mode.

## 2.0.0

- Renamed from `ste80` to `humanizer-ste80`. The skill is now a general humanizer that uses STE80 as its method.
- New Part 1: 23 AI tells in five groups (staging, rhythm, inflation, formatting, chat residue), inspired by Wikipedia's "Signs of AI writing" and blader/humanizer.
- Part 2: the 23 STE80 structure rules, now in compact form. The full rules with before and after examples moved to `references/ste80-rules.md`.
- New modes: Humanize (default), Light, Strict STE.
- New sections: Voice (match a writing sample), "Human quirks" to keep, contradiction flag in the fidelity rules.
- `ste_check.py` now also flags AI tells: not-X-but-Y, chatbot openers and closers, run-ups, fake depth, stacked hedges, vague authority, "-ing" riders, inflated significance and curly quotes.
- New eval case: `humanize-linkedin-post`.

## 1.0.0

- First release.
- 80% mode (default) and strict mode.
- 23 rules in six groups (sentences, verbs, words, structure, punctuation, what 80% relaxes), with before and after examples.
- Fidelity rules: keep every fact, keep uncertainty at its strength, add nothing.
- `references/word-swaps.md`: plain alternatives in ten groups, including typical LLM vocabulary.
- `references/strict-mode.md`: paraphrased ASD-STE100 Issue 9 rule sections and a final checklist.
- `scripts/ste_check.py`: dependency-free heuristic linter.
