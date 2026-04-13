# Detailed workflows

Use this file when the main task is complex, the user expects a polished handoff, or the skill repository has more than a few files.

## Source priority

Use sources in this order unless the user explicitly wants a pinned snapshot:

1. Official Agent Skills LLM docs (`https://agentskills.io/llms-full.txt`)
2. OpenAI Codex docs for Codex-specific behavior
3. `vercel-labs/skills` for `npx skills` installation and packaging ergonomics
4. The user’s repository, attachments, and linked skill source
5. Your own judgment for gaps, tradeoffs, and proposed fixes

When you rely on your own judgment, label it as judgment instead of presenting it as documented behavior.

## Creation mode

### 1. Capture the job

Extract:

- What recurring task the skill should handle
- Inputs the agent will receive
- Outputs or artifacts the user expects
- What should trigger the skill
- What should *not* trigger the skill
- Whether the work is instruction-only or needs scripts/templates

### 2. Shape the scope

A good skill covers one coherent unit of work.

Good patterns:

- one repeatable workflow
- one domain integration
- one stable review/audit process
- one file- or artifact-oriented job

Bad patterns:

- “all engineering best practices”
- multiple unrelated workflows forced into one skill
- a generic prompting style with no concrete task boundary

### 3. Design the files

Default structure:

- `SKILL.md` for always-needed instructions
- `references/` for deeper guidance and checklists
- `assets/` for templates or example outputs
- `scripts/` only when deterministic behavior or repeated validation is worth the extra complexity
- `agents/openai.yaml` only when Codex metadata, dependencies, or invocation policy adds value

### 4. Write the trigger description

The description is the primary trigger surface. Make it concrete.

Include:

- what the skill does
- when it should be used
- task keywords and adjacent phrasings
- boundaries or “do not use” cues when they prevent false positives

Avoid:

- vague claims such as “helps with X”
- only naming a file format without the actual jobs
- broad descriptions that would activate on unrelated tasks

### 5. Draft the body

Favor imperative instructions and reusable output contracts.

Strong pattern:

- When to use
- Do not use when
- Workflow
- Deliverables
- References
- Failure modes

### 6. Package the handoff

Default deliverable set:

1. Finished skill folder
2. ZIP artifact
3. Short changelog
4. Assumptions / unresolved risks
5. Install notes only if they help

## Audit mode

### What to inspect

Review all materially relevant files in the skill area:

- main `SKILL.md`
- `agents/openai.yaml`
- `scripts/`
- `references/`
- `assets/`
- tests or evals
- helper docs or companion files that change how the skill works

Only pull in repo-level files when they materially affect installation, execution, conventions, or evaluation.

### How to audit

1. Read the trigger description first.
2. Check the frontmatter against spec constraints.
3. Check whether the body is concise and specific enough.
4. Verify the skill’s references and scripts are actually reachable and useful.
5. Look for hidden assumptions, broken file references, unsupported dependencies, and unbounded instructions.
6. Check whether the skill can actually be installed and discovered by the target agent.
7. Assess evaluation readiness: trigger tests, output assertions, or at least a credible manual test plan.

### Preferred audit structure

- Summary
- Key Issues
- Fixes
- Optional: Rewritten Sections
- Optional: Unverified / Missing Context

Keep audits concise. Severity order matters more than volume.

## Improvement mode

Use improvement mode when the skill is fundamentally sound but underperforming.

Prioritize:

1. broken or misleading triggers
2. incorrect or unstable instructions
3. missing failure handling
4. installability / portability issues
5. unnecessary verbosity
6. polish

Preserve:

- skill name
- folder structure
- author voice
- working parts

Change these only when there is a strong correctness or usability reason.

## `skills.sh` handling

Treat a `skills.sh` page as an entry point, not a full audit target.

Workflow:

1. Open the page.
2. Identify the skill name and linked GitHub repository.
3. Inspect the actual skill directory in the repository.
4. Audit the repo files that shape behavior, not just the landing-page summary.

## Missing context

When the full package cannot be retrieved:

- say exactly what you could inspect
- say what remains unverified
- still provide the strongest practical revision you can
- avoid confident claims about files you have not seen
