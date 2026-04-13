# Finish Checklist

Use this checklist when the closeout path spans multiple systems or before taking an irreversible action.

## 1. Confirm the Finish Line

- [ ] Decide what counts as done in this repo: branch push, PR update/open, merge, release/tag, deploy/publish, production verification, tracker update, and/or handoff note.
- [ ] Confirm which outcomes are implied by repo context and the user's wording.
- [ ] If the highest-risk target is ambiguous, ask once before acting.

## 2. Preflight

- [ ] Check git status and current branch.
- [ ] Check PR/review state and branch protection rules.
- [ ] Check CI, tests, lint, build, and typecheck signals that matter for the intended finish line.
- [ ] Check release/deploy config plus any required secrets, credentials, or approvals.
- [ ] Check whether repo-native tooling is configured, such as release automation, Entire checkpoints, tracker bots, or changelog generators.
- [ ] Note any migrations, feature flags, rollout steps, or rollback notes that are already part of the repo's normal closeout.

## 3. Validate

- [ ] Run the smallest validation set that is still trustworthy for the finish line.
- [ ] Fix only finish-blocking issues.
- [ ] Re-run failed gates after each fix.
- [ ] Do not ignore a failing gate unless repo policy explicitly allows it; if you must proceed, call out the exact skipped check and risk.

## 4. Execute

### Branch / PR Finish

- [ ] Push the branch if needed.
- [ ] Open or update the PR with the right summary and linked tracker items.
- [ ] Resolve or document review blockers that are actually in scope.

### Merge / Release / Deploy / Publish Finish

- [ ] Follow the repo's documented order of operations.
- [ ] Use existing automation instead of improvising manual steps.
- [ ] Stop if the environment, target, or required approval is unclear.

## 5. Clean Up Surfaces

- [ ] Update tracker/issues/tasks/status notes required by the workflow.
- [ ] Update release notes or changelog only if the workflow calls for it.
- [ ] Delete or keep branches according to repo convention.
- [ ] Ensure expected checkpoints, artifacts, or logs are present.
- [ ] Leave a short handoff note when it prevents next-day confusion.

## 6. Report Back

Include:

- what landed
- where it landed
- what you verified
- what systems you updated
- any blocker, skipped gate, residual risk, or next action

## Stop Conditions

Stop and ask when:

- the irreversible target is unclear,
- required approval or credentials are missing,
- a production-impacting gate is failing and no safe fix is obvious, or
- the task has turned into substantial new implementation rather than closeout.
