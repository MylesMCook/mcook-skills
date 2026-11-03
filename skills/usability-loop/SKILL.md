---
name: usability-loop
description: Iterate on a running web app until a fresh first-time-user tester rates its usability 9/10. Each round a new, blind subagent tries real tasks in the browser and scores them; the main agent fixes what it reports and repeats. Use when the user asks for usability rounds, a first-time-user test loop, "keep going until it's a 9/10", or a dummy user rating the app.
---

# Usability loop

## 1. Set up (once, before round 1)

Settle these, then run the loop without check-ins except where step 3 says to stop:

- **App URL.** The app must be running locally or on a test host. Start it with the project's own dev command if needed.
- **Persona.** One or two sentences: who they are, what they know, what they don't. Default: "a capable adult who has never seen this app and has no help."
- **Tasks.** 3 to 5 real jobs a new user must do, phrased as goals in the user's words, not the app's labels ("Add a customer and find them again", not "click New Client"). Infer them from the README, routes and UI, then show them to the user for approval. Tasks are product intent, so the user owns them.
- **Sign-in.** If needed, use test credentials from the project's seed or example config only.
- **Reset.** Find how to reset the app's test data (seed script, fresh database, test account). Records left by an earlier tester reveal earlier rounds. If there's no safe, documented reset or test login, ask the user. Never delete data the loop didn't create.
- **Browser tool.** Run `playwright-cli --version`. If it's missing, ask the user; install nothing. If a tester stalls on permission prompts, ask the user to allow `playwright-cli` commands.

Freeze the persona, tasks and rubric for the whole loop. Changing them mid-loop to get a pass invalidates the result.

## 2. Run a round

Before each tester:

1. Run `playwright-cli close` and reset the test data.
2. Delete the `.playwright-cli/` folder in the working directory if it exists, so old snapshots don't leak.

Then spawn a **new** subagent with no conversation history (Claude Code: `general-purpose`, model `sonnet`) using the tester prompt below. If you can't start a fresh agent, stop and tell the user; never act as the tester yourself.

Never tell the tester the target score, the round number, earlier scores, or what changed, including in session names. A tester that knows it's round 4 rewards effort.

### Tester prompt

```
You are using this web app for the first time. Persona: <persona>

App: <url>
<test credentials, if any>

Tasks:
<numbered task list, as approved>

Run `playwright-cli --help` for command syntax; read no other docs, source
files or repo. If the command is unavailable, stop and return
TOOL_UNAVAILABLE. Install nothing.

Use the browser only the way a sighted user would:
- Use only these commands: open <url>, screenshot, find, click, dblclick,
  fill, type, press, select, check, uncheck, hover, drag, upload,
  mousewheel, dialog-accept, dialog-dismiss, tab-list, tab-select,
  go-back, reload, close.
- On each new screen, take a screenshot and open the image file to look at
  it. Choose what to act on from the screenshot alone, then get its ref
  with `find "<text you can see>"`. Scroll to see more. If the target has
  no visible text, report it as an unclear label.
- If a task takes more than about 15 actions or you're going in circles,
  mark it FAILED and move on. If a task needs an earlier task that failed,
  mark it FAILED (blocked by task N) without trying.

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

Issue severity: blocker = a task FAILED; major = caused a backtrack, guess
or detour; minor = anything else.

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
- **Cap:** at most 5 tester rounds, counting failed confirmations. Never fix after round 5; report. If round 5 passes, still run its confirmation.
- **Plateau:** from round 3 on, stop if the best overall score hasn't improved in the last 2 rounds. A single score can drift by a point, so compare against the best, not the previous round.

## 5. Report

- Final scores from the last two testers, and the round log
- What changed in the app, in user terms
- Remaining issues and any product decisions needed
- If you stopped on the cap or a plateau, say so plainly; don't round up
