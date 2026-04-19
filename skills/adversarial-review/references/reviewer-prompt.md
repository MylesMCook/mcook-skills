# Reviewer Prompt Template

Every reviewer prompt should include six blocks, in this order:

1. **Intent**
   One sentence on what the author is trying to achieve.
2. **Lens**
   Copy the full assigned lens text from `references/reviewer-lenses.md`.
3. **Repo principles**
   Include the exact contents of whichever project rules actually exist and matter: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `brain/principles.md`, or equivalent files.
4. **Review scope**
   Specify the diff, staged changes, branch, file list, or plan being reviewed.
5. **Evidence packaging**
   Provide the smallest useful context: touched files, adjacent files, and any large diff or plan text via stdin or an attached context file.
6. **Output contract**
   Tell the reviewer exactly how to format findings.

## Required reviewer behavior

Use this behavior in every prompt:

- You are an adversarial reviewer. Find real problems, not style nits.
- Stay read-only. Do not edit files, write plans, commit anything, or suggest mutating commands as part of the review.
- Prioritize issues that would block ship, create data loss, break correctness, widen security risk, or add avoidable complexity.
- Cite files and line numbers whenever available.
- If you claim a CLI flag, auth behavior, or runtime detail is wrong, name the exact flag or behavior and cite the failure evidence you inspected.
- If you are uncertain, say why and what evidence is missing.
- Return only markdown in this structure:

```markdown
1. **[high|medium|low]** Short title — file:line
   - Why it matters:
   - Failure scenario:
   - Recommendation:
   - Confidence: high|medium|low
```

- If nothing worth reporting survives your own skepticism, end with `No material findings.`

## Harness-specific packaging

### Claude Code

Keep the prompt short. Give intent, lens, review scope, and the output contract. Let Claude inspect files with `Read`, `Grep`, and `Glob` instead of pasting large excerpts.

### Codex subagent

When the host is Codex, spawn a fresh subagent for the Codex reviewer. Keep the prompt compact, include the repo root, lens, review scope, read-only instruction, and output contract, and point it at context file paths instead of inlining large diffs or logs.

### Codex CLI fallback

Use this only when the host is not Codex or a fresh Codex subagent is unavailable. Keep the repo root as the working directory. If the diff, logs, or plan text are large, pipe them through stdin or attach them as a separate context file rather than inlining everything into the prompt.

### Gemini CLI

Keep Gemini in read-only plan mode. State explicitly:

- do not create or edit plan files
- do not exit plan mode
- do not implement anything

Pass large diff or plan text through stdin, and prefer precise file references over broad repo dumps.

## Minimal scaffold

```markdown
Intent:
<one sentence>

Lens:
<paste assigned lens>

Repo principles:
<paste exact principles or say "None provided.">

Review scope:
<what to inspect and where to start>

Instructions:
You are an adversarial reviewer. Find real problems, not style nits.
Stay read-only.
Cite files and lines when possible.
Return only markdown findings in the required structure.
If no material findings remain after your own skepticism, say: No material findings.
```

Spawn reviewers in parallel when the environment allows it.
