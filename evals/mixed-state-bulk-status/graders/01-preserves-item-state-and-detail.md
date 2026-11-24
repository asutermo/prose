---
type: llm
focus: trace
weight: 1
---

status.md contains all three items in a scannable list or table. Their names or distinguishing actions appear near the start of each item. Structure and terminology are consistent, but each item's state remains distinct:

- Login retry fix is completed and released in version 2.4.1, with 6 reports closed.
- Search timeout investigation is active, with reproduction in progress and 3 traces so far. It has no fix yet.
- Export format review is planned for December 4 and has not started.

Pass only if all these facts stay attached to the correct item. Allow explicit state labels or verbs that convey the same states. Fail if a shared tense or summary turns any planned or active work into completed work, or any completed work into pending work. Fail if the output adds versions, dates, counts, examples, owners, outcomes, or other facts to fill a uniform template. Omitted fields or fields marked "not provided" are acceptable. Absence of a count is not evidence of zero.
