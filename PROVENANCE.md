# Provenance

What in this repository is whose work. The short version: prose is a standalone skill that started from Dodaios/ste80-humanizer v4 (MIT). A large part of its body text is that project's work, reused verbatim under the MIT license. This file says exactly which parts.

## Verbatim from Dodaios/ste80-humanizer v4 (MIT, https://github.com/Dodaios/ste80-humanizer)

- `references/ai-tells.md` - full entries for AI tells §1 to §26 (Watch for, Problem, Before, After), plus a header note pointing to §27 to §31 in SKILL.md, which this repo added.
- `references/ste80-rules.md` - full entries for the STE80 structure rules S1 to S15.
- `references/word-swaps.md` - the plain-word swap list.
- `references/strict-mode.md` - the strict rule set and checklist.
- `references/worked-example.md` - the worked Pass 1 / Pass 2 example.
- `scripts/ste_check.py` - the linter, unchanged.
- `evals/` - all four eval cases and graders, unchanged.
- `assets/ste100-overview.png` - the STE overview graphic.
- `LICENSE` - the MIT license text.
- `SKILL.md`, roughly 80 percent: the method tables for Pass 1 §1 to §26 and Pass 2 S1 to S15, the modes, the how-to-work steps, the fidelity rules, the voice guidance, and the when-not-to-act list are Dodaios's text. The method itself is Andrej Karpathy's "80% of the way to ASD-STE100" idea.

## Added in this repository (v5.0.0 and v5.1.0)

- `SKILL.md` Part 1, §27 to §31: showmanship and false depth, from blader/humanizer patterns 30-34.
- `SKILL.md` Part 2: the five readability principles for bulk text, summarized from Shreya Shankar's Full Stack Data Lab post (October 29, 2026). Wording is ours.
- `SKILL.md` Part 3: the PR body template, adapted from Humanlayer's show-me skill (MIT), and the commit message rules.
- `SKILL.md` Part 4 and `references/user-facing-docs.md`: user-facing docs rules, adapted from landaire/config CLAUDE.md. Wording is ours.
- `README.md`: rewritten for the merged scope.
- `CHANGELOG.md` entries for 5.0.0 and 5.1.0, `AGENTS.md` edits, `THIRD_PARTY_NOTICES.md` additions, and the `agents/openai.yaml` display strings.
- The name and the merged three-part structure.

## License position

The Dodaios, blader/humanizer and Humanlayer material is MIT-licensed. Reuse with the license and copyright notice preserved is permitted, and `LICENSE` plus `THIRD_PARTY_NOTICES.md` do that. The landaire and Full Stack Data Lab material is credited as the source of the method. The wording here is adapted, not copied.

## Relation to the upstream skill

`prose` is not a fork of Dodaios/ste80-humanizer and does not represent it. The upstream repo remains the home of the STE-only variant, unchanged.
