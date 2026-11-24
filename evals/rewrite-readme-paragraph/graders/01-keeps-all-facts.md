---
type: llm
focus: trace
weight: 1
---

rewritten.md preserves Redis, "up to 60%" with "most cases", automatic invalidation on write, POST /v2/import, cache.flush(), bulk writes not currently tracked by invalidation hooks, the default TTL of 300 seconds, and its override through CACHE_TTL.

Preserve the possibility that users may need to call cache.flush() manually after POST /v2/import. Do not turn "may need to" into an unconditional requirement, a guarantee, or an instruction to always flush. A qualification elsewhere does not excuse a contradictory command.

The source's "stale data is never served" guarantee conflicts with its untracked bulk writes and possible manual flush. Preserve both statements as source claims and flag the conflict in a note, following the skill's fidelity rule. Do not silently repair or qualify the source's guarantee, erase the bulk-import exception, or invent how the system resolves it.
