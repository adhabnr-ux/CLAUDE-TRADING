# Control Switch — both Bulls read this FIRST, every run

The human edits this file (directly on GitHub — web or mobile app) to control
both agents at the start of the next synced run, without touching the cloud
environments. It is not an out-of-process mid-run kill switch. Agents obey it
but **never** edit it.

STATUS: RISK_OFF

NOTE: Institutional risk-foundation rollout in progress. Keep scheduled broker
mutations disabled until the draft PR is reviewed, both account fingerprints
are configured, the trusted earnings calendar is populated, and read-only
reconciliation passes for each paper account.

## Valid STATUS values

- `ACTIVE` — normal operation.
- `RISK_OFF` — open NO new positions (either Bull). Managing exits, stop
  audits, journaling, and notifications all continue.
- `PAUSED` — place NO orders of any kind. Journal "paused by human", send the
  routine's notify saying so, commit, and stop.

## Optional note to the agents

Add a line starting with `NOTE:` and both Bulls will read it at the start of
their next run and acknowledge it in their journal.

## Asking Bull a question

Add a line starting with `QUERY:` and the next routine to run will read it,
include a paragraph answer in its Telegram notify, and leave this file unchanged.
The human clears the line after reading the answer. Bull does NOT trade on a
query — answers only.

## Cross-Bull learning trigger

If Aggressive Bull beats Cautious Bull by more than 5 percentage points
(since-inception return) for **2 consecutive weekly reviews**, Cautious Bull's
next weekly review must journal one specific lesson learned from AGGRO and
propose one concrete rule change (sizing, deployment pace, watchlist, or
exit). Set the line below to `TRIGGERED: <date>` when this condition first
fires; clear it once the lesson is journaled. Both Bulls read this line.
Only the human sets or clears this field; agents report completion elsewhere.

CROSS_BULL_LEARNING:
