# Decision log

Keep this file in your repository and commit changes to it as you go. It is
assessed, and it is the raw material for your technical commentary.

## Why this exists

Your Component 1 commentary has to answer four questions:

| Commentary question | Where it comes from in this log |
|---|---|
| Why does each pipeline stage exist? | The **Context** and **Decision** fields of your D entries |
| One significant trade-off, and the alternative you rejected | The **Alternatives** field of your D entries |
| One failure you hit, and how you diagnosed it | Your **F** entries |
| The operational limitations of your pipeline | The **Consequences** field of your D entries |

Fill this in properly as you go and the commentary largely assembles itself.
Leave it until Week 10 and you will be reconstructing your own reasoning from
memory, which is harder and reads worse.

## How to use it

- **One entry per real decision.** Not every command you ran — every choice
  where you could reasonably have done something else.
- **Write it the week you make it.** Commit the entry in the same week. Your
  commit history shows when you wrote it, and a log written entirely in the
  final week is visible.
- **Number entries in order.** D-001, D-002. Never renumber; if you change
  your mind, add a new entry and mark the old one superseded.
- **Short is fine.** Four or five sentences per field is plenty. Reasoning
  matters, not word count.
- **Minimum:** one entry per week from Week 5 onward, plus at least one F
  entry. Most students end with 8 to 12 entries. Decisions you made in Weeks
  2 to 4 can be added retrospectively — mark them `(backfilled)`.

---

## Decisions

<!-- Copy the block below for each new decision. -->

<!--
## D-00n — <short title, e.g. "Use a multi-stage Docker build">

- **Week:**
- **Status:** accepted
- **Stage:** build | test | containerise | publish | deploy | infrastructure | security | other

**Context.** What was the situation? What made a decision necessary here?

**Decision.** What did you do?

**Alternatives.** What else could you have done, and why did you reject it?

**Consequences.** What does this make easier? What does it make harder, more
expensive, or impossible later?

**AI use.** Which tool, what you asked for, and what you did with the answer.
Write "none" if you did not use one.
-->

## D-000 — EXAMPLE ENTRY, DELETE BEFORE SUBMISSION

- **Week:** 3
- **Status:** accepted
- **Stage:** build

**Context.** The CI workflow was re-downloading every dependency on each run,
which pushed the build to just over four minutes. Northgate has two
infrastructure staff and no appetite for a pipeline people avoid running.

**Decision.** Added dependency caching to the workflow, keyed on the lockfile.
Build time dropped to about 50 seconds on a cache hit.

**Alternatives.** Considered leaving it — four minutes is tolerable in a
cohort project. Rejected because the whole argument I am making to Northgate
is that a slow pipeline changes team behaviour, and it would be inconsistent
to ship one. Also considered committing the dependencies to the repository,
which is faster still but makes the dependency scanning in Week 6 meaningless.

**Consequences.** Faster feedback, so I actually run it. But the cache key is
tied to the lockfile, so a corrupted cache would need manual clearing — that
is a manual step I have reintroduced, and someone at Northgate would need to
know it exists.

**AI use.** Asked Claude for the caching syntax for this CI platform. Checked
it against the platform documentation before committing, because the first
version it gave used a deprecated action version.

---

## Incidents

Something broke. Record it here, whether you caused it or found it.

<!--
## F-00n — <what appeared to be wrong>

- **Week:**
- **Stage:**

**Symptom.** What did you observe? What told you something was wrong — a red
pipeline, a failing test, a customer-visible fault, nothing at all?

**Diagnosis.** How did you work out what was actually happening? What did you
check, in what order, and what ruled things out?

**Cause.** What was actually wrong.

**Fix.** What you changed.

**What would have caught it sooner.** Be honest. Sometimes the answer is
"nothing in my current pipeline would have caught this", and that is a finding
worth writing down.
-->

---

## Generative AI declaration

Required. See the Assessment Guidance. Summarise your overall use here, in
addition to the per-entry notes above.

| Tool | Used for | How you checked the output |
|---|---|---|
|  |  |  |
