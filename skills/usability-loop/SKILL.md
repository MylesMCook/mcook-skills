---
name: usability-loop
description: Iterate on a running web app until a fresh first-time-user tester rates its usability 9/10. Each round a new, blind subagent tries real tasks in the browser and scores them; the main agent fixes what it reports and repeats. Use when the user asks for usability rounds, a first-time-user test loop, "keep going until it's a 9/10", or a dummy user rating the app.
---

# Usability loop

An evaluator-optimizer loop. A fresh tester judges, you fix, repeat. The loop only works if the tester stays blind and strict, so most of this skill is guardrails against score inflation.

## 1. Set up (once, before round 1)

Settle these, then run the loop without check-ins except where step 3 says to stop:

- **App URL.** The app must be running locally or on a test host. Start it with the project's own dev command if needed.
- **Persona.** One or two sentences: who they are, what they know, what they don't. Default: "a capable adult who has never seen this app and has no help."
- **Tasks.** 3 to 5 real jobs a new user must do, phrased as goals, not clicks ("Add a customer and find them again", not "click New"). Infer them from the README, routes and UI, then show them to the user for approval. Tasks are product intent, so the user owns them.
- **Sign-in.** If needed, use test credentials from the project's seed or example config only.
- **Reset.** Find how to reset the app's test data (seed script, fresh database, test account). Records left by an earlier tester reveal earlier rounds.
- **Browser tool.** Run `playwright-cli --version`. If it's missing, ask the user; install nothing. Confirm a subagent can run `playwright-cli` commands without permission prompts, or the loop will stall.

Freeze the persona, tasks and rubric for the whole loop. Changing them mid-loop to get a pass invalidates the result.

## 2. Run a round

Before each tester:

1. Run `playwright-cli close-all` and reset the test data.
2. Delete the `.playwright-cli/` folder in the working directory if it exists, so old snapshots don't leak.

Then spawn a **new** subagent with no conversation history (Claude Code: `general-purpose`, model `sonnet`) using the tester prompt below. Never reuse or message a previous tester.

Never tell the tester the target score, the round number, earlier scores, or what changed, including in session names. A tester that knows it's round 4 rewards effort.

### Tester prompt

```
You are using this web app for the first time. Persona: <persona>

App: <url>
<test credentials, if any>

Tasks:
<numbered task list, as approved>

Load the playwright-cli skill; it is the only doc you may read. If the
command is unavailable, stop and return TOOL_UNAVAILABLE. Install nothing.

Use the browser only the way a sighted user would:
- Allowed: open <url>, snapshot, screenshot, click, fill, type, press,
  select, check, uncheck, hover, go-back, reload, close. Target elements by
  snapshot refs only.
- Not allowed: eval, run-code, console, requests, route, cookie or storage
  commands, webmcp tools, CSS selectors or test IDs, or goto to any URL you
  weren't given. Do not read source files, the repo, or any docs.
- On each new screen, take a screenshot and judge clarity from what it
  shows. Use the snapshot only to find refs.

Attempt each task in order. For each task, write as you go:
- What you expected vs what happened
- Every hesitation, wrong turn, backtrack, unclear label, missing feedback,
  error, or dead end, with where it happened (page, element text)
- Outcome: DONE_CLEAN, DONE_WITH_STRUGGLE, or FAILED

Then, after all tasks, write your reasoning first and only then the scores.

Rubric (per task):
10 done first try, nothing to report
9  done unaided, at most one brief hesitation, no backtracking
7-8 done, but needed a backtrack or a guess
5-6 done only through trial and error or a long detour
3-4 failed or blocked
1-2 could not get started

Overall score: your judgment of the whole app, but never more than the
lowest task score + 1. Be strict; a 9 means a stranger would succeed
without help.

Return exactly:
## Tasks
### <task> - <outcome> - <score>/10
<notes>
## Issues
- [blocker|major|minor] <where>: <what went wrong> (task N)
## Reasoning
<why these scores>
## Overall: N/10
```

## 3. Fix

- Fix only issues the tester reported, blockers first, then majors. Minor issues only once no blockers or majors remain.
- Do not add features the tester didn't need. Do not fix by adding instructions or tooltips when a clearer label or flow would do.
- If a blocker or major needs a product decision (what a field means, whether a step should exist), stop the loop and ask the user before the next round. Collect minor ones for the report.
- Run the project's tests after fixing. Restart or rebuild the app if the change needs it.

Keep a one-line-per-round log in the conversation: round, overall, task scores, top issues fixed.

## 4. Stop

A tester **passes** when its overall score is 9 or higher and it reports no blocker or major issue.

- **Confirm:** when a tester passes, run one confirmation tester: fresh, same prompt, a stronger model if available (Claude Code: `opus`). If it also passes, you're done. If not, treat its report as the next round's findings, fix and continue; it counts as a round.
- **Cap:** at most 5 tester rounds, not counting a final confirmation that passes. Don't fix after the last round; report.
- **Plateau:** from round 3 on, stop if the best overall score hasn't improved in the last 2 rounds. A single score can drift by a point, so compare against the best, not the previous round.

## 5. Report

- Final scores from the last two testers, and the round log
- What changed in the app, in user terms
- Remaining issues and any product decisions needed
- If you stopped on the cap or a plateau, say so plainly; don't round up
