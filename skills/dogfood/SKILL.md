---
name: dogfood
description: >
  Formal repro-first browser QA for real web apps. Use when the user wants to
  dogfood a site, run QA, bug hunt, find issues, or test an app with
  handoff-grade evidence such as repro steps, screenshots, videos, and a
  structured report. Do not use for lighter exploratory passes where
  `browser-probe` is enough.
---

# Dogfood

Use this skill when the job is not just to explore, but to hand back issues with proof.

## Defaults

- Require only the target URL unless auth is mentioned.
- Use `agent-browser` directly, never `npx agent-browser`.
- Default scope is the full app.
- Default output directory is `./dogfood-output/`.
- Default session name is a slugified target name.

## Workflow

1. Initialize the output directory, screenshots directory, videos directory, and report file from `templates/dogfood-report-template.md`.
2. Authenticate only if needed. If the flow needs OTP or email codes, stop and ask the user for that code.
3. Orient on the app with an annotated screenshot and a fresh interactive snapshot.
4. Explore the app systematically using `references/issue-taxonomy.md` to decide what to check and how severe a finding is.
5. Document each issue immediately before moving on. Do not batch findings for later.
6. Wrap up by reconciling severity counts, closing the session, and summarizing the most important issues.

## Evidence Rules

- Interactive or behavioral issues need a repro video plus step-by-step screenshots.
- Static issues visible on load need one annotated screenshot. Set repro video to `N/A`.
- Verify reproducibility before collecting evidence. Retry once before calling it a real issue.
- Use `type` during recorded repros when human pacing matters. Use `fill` outside recording when speed matters.
- Check `console` and `errors` during the run so console-visible failures do not get missed.

## Output Contract

- Produce one structured report using `templates/dogfood-report-template.md`.
- Append findings as they are discovered so interrupted runs still leave usable output.
- Aim for a small set of well-documented issues rather than a long vague list.
- End by telling the user the report path, total issue count, severity breakdown, and the most critical items.

## References

- `references/issue-taxonomy.md` - severity calibration and what to look for
- `templates/dogfood-report-template.md` - report scaffold

## Guardrails

- Keep one live `agent-browser` session for the run unless recovery forces a restart.
- Never read the target app's source code while dogfooding it.
- Do not turn this into generic browser automation. This skill is for issue-finding with handoff-grade evidence.
- Route lighter exploratory requests to `browser-probe`.
