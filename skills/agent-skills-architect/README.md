# Agent Skills Architect

A Codex-oriented skill for creating, auditing, improving, and packaging Agent Skills.

## Included

- `SKILL.md`
- `agents/openai.yaml`
- `references/` for workflows, checklists, install notes, and eval guidance
- `assets/` for starter files

## Typical install options

Repository-local authoring:

- place the folder under `.agents/skills/`

Cross-agent or Codex-targeted installation:

```bash
npx skills add <repo-or-path> --skill agent-skills-architect -a codex
```
