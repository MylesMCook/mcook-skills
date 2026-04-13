---
name: agent-skills-architect
description: Create, audit, improve, rewrite, or package Agent Skills and Codex skills. Use when the task involves a SKILL.md-based skill, trigger descriptions, frontmatter, agents/openai.yaml, skills.sh listings, npx skills installation, or producing an updated skill ZIP. Do not use for general software architecture or unrelated code review.
---

# Agent Skills Architect

Create, audit, improve, and package Agent Skills with a Codex-first workflow.

Designed for OpenAI Codex and compatible Agent Skills clients. Works best with repo filesystem access; optional network access helps verify live docs and linked repositories.

## Use when

- The user wants a new skill from an idea, workflow, repeated task, or rough notes.
- The user wants an existing skill reviewed, fixed, tightened, repackaged, or made more installable.
- The request mentions `SKILL.md`, skill descriptions, trigger behavior, `agents/openai.yaml`, `skills.sh`, `npx skills`, Codex skills, or skill ZIPs.

## Do not use when

- The request is general software architecture or code review unrelated to skills.
- The task is about a plugin, MCP server, or app integration with no skill design or review component.

## Operating stance

- Prefer documented guidance over memory. Start with the official Agent Skills LLM docs at `https://agentskills.io/llms-full.txt`, then Codex docs for Codex-specific behavior, then the `vercel-labs/skills` repository or README for `npx skills` installation ergonomics.
- Separate documented guidance from your own judgment.
- Preserve the author's working parts, folder structure, name, and voice unless there is a strong reason to change them.
- Prefer minimal, high-leverage edits over broad rewrites.
- If the user gives a `skills.sh` URL, treat it as an entry point. Resolve the linked repository and inspect the actual skill directory before judging it.
- If live docs, linked repositories, or supporting files are unavailable, say what is unverified and continue with the best evidence you have.
- Use scoring only if the user explicitly asks for it.

## Workflow

1. Decide the mode: create, audit, or improve.
2. Inspect all materially relevant files:
   - `SKILL.md`
   - `agents/openai.yaml`
   - `scripts/`, `references/`, `assets/`
   - helper scripts, tests, evals, and nearby docs that affect installation, behavior, or evaluation
3. Keep `SKILL.md` concise. Put only always-needed instructions there. Move heavy detail into references. Use `references/checklists.md` and `references/workflows.md`.
4. Prefer instruction-only skills unless deterministic behavior, validation, or external integration clearly justifies scripts.
5. When you can materially improve the result, return an updated skill folder and a ZIP instead of critique alone.
6. When information is incomplete, make a safe best effort instead of stalling.

## Modes

### Create

- Extract the reusable workflow, inputs, outputs, triggers, non-triggers, dependencies, and likely failure cases.
- Draft a precise `name` and `description`.
- Choose the smallest skill that covers one coherent unit of work.
- Put always-needed instructions in `SKILL.md`; move deeper guidance to references.
- Add `agents/openai.yaml` only when Codex-specific metadata or policy meaningfully helps.
- Include templates or assets only if they save repeated work.

### Audit

Use this structure unless the user asks for something else:

- Summary (2-4 lines)
- Key Issues (ordered by severity)
- Fixes (paired to issues, concrete and actionable)
- Optional: Rewritten Sections
- Optional: Unverified / Missing Context

During the audit:

- Check trigger precision first: description, scope, and boundaries.
- Check progressive disclosure: is `SKILL.md` trying to do too much?
- Check maintainability: layout, naming, references, scripts, failure handling, and hidden assumptions.
- Check installability: folder name, frontmatter validity, portability, and whether agent-specific config is justified.
- Check evaluation: are there trigger tests, output assertions, or at least a credible eval plan?

### Improve

- Prioritize the smallest set of changes that most improves correctness, trigger behavior, reliability, and DX.
- Show before/after snippets when useful.
- Preserve the existing skill's intent.

## Deliverables

Default handoff order:

1. Updated skill folder or rewritten sections
2. ZIP artifact when possible
3. Concise changelog
4. Important assumptions, unresolved risks, or unverified areas
5. Brief install or usage notes only when materially helpful

## References

- `https://agentskills.io/llms-full.txt` — primary upstream Agent Skills documentation
- `references/workflows.md` — detailed create, audit, and improve playbooks
- `references/checklists.md` — frontmatter, structure, scripts, and packaging checks
- `references/codex-install.md` — Codex-specific placement, invocation, and `npx skills` notes
- `references/evals.md` — trigger and output evaluation guidance
- `assets/` — starter templates for new skills and audit/eval outputs

## Failure modes

This skill has failed if it:

- produces generic advice instead of concrete, evidence-backed changes
- ignores relevant files outside `SKILL.md`
- rewrites a working skill unnecessarily
- makes unverified claims about current docs or CLI behavior
- returns only critique when an improved artifact was feasible
