---
type: llm
focus: trace
weight: 1
---

runbook.md preserves these literals exactly as supplied: `./migrate.sh --env=prod`, `./rollback.sh 2026.11`, `Ctrl+C`, `#ops`, `30 minutes`, and `10-15 minutes`. Keep the usual duration distinct from the abort threshold. Do not change `10-15` to `10 to 15` or treat 15 minutes as the abort threshold.
