# User-facing docs rules

Source: adapted from the user-facing docs section of landaire/config `CLAUDE.md` (https://github.com/landaire/config). SKILL.md Part 4 is the compact table. This file has the full rules with the reasoning.

## The default reader is a user

Assume the reader wants to use the project, not audit it. Every rule below follows from that. Audit-oriented material (threat models, internals, exhaustive option coverage) belongs in a developer doc that the README links to, not in the README itself.

## Structure

- **tl;dr first.** Open with a short bullet list of what the project does for the reader: what they get, what they need, how to start. Five bullets or fewer.
- **Usage before contributor material.** Build, test and contributing sections come last. A reader who wants to run the thing should not scroll past CI instructions to find the install command.
- **Common case first.** Give the setup that works for most readers, with one example. Rare setup steps (unusual OSes, air-gapped installs, legacy versions) go in a linked doc.
- **No exhaustive lists.** A feature table, module inventory or version-range matrix is developer material. Name the categories and link for detail.

## Content

- **Leave out internal detail.** Addresses, flags, module inventories, test counts and benchmark results do not help a user decide to use the project or start it.
- **Say why.** When a step or requirement is not obvious, one short clause says why it exists. Reasoning prevents cargo-culting and wrong workarounds.
- **Link on first mention.** Every external tool or project gets a link the first time it appears, so a newcomer does not have to search.

## Voice and formatting

- **Plain voice.** "You" for the reader, "we" or "I" for the author. No stilted nominalizations ("the optimizations of the release profile" - say "the release is faster because...").
- **One idea per sentence.** Do not chain clauses with semicolons or colons. Split them into sentences, or into bullets when they are parallel items.
- **No hard-wrapped prose.** Write one line per paragraph. Wrapping at 80 columns is a diff artifact, not a reading aid. Let the renderer wrap.
- **American English only.** No "colour", "favour", "centre".
