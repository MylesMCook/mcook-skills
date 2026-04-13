# Evaluation guidance

Use this file when the user asks for a better description, stronger trigger behavior, or a test plan.

## Trigger evaluation

Write a small set of prompts before finalizing the description.

Include both:

- prompts that should trigger
- prompts that should not trigger

Aim for realistic requests, not toy phrasing.

Questions to ask:

- would the skill activate when the user does not know the exact skill name?
- would the skill avoid activating on adjacent but different work?
- does the description mention the jobs users actually ask for?

## Output evaluation

For output quality, define concrete assertions.

Good assertions are:

- observable
- countable
- specific
- not brittle to harmless wording differences

Weak assertions are:

- “the result is good”
- “the writing sounds nice”
- any claim that cannot be checked from the output

## Minimal eval loop

1. Draft the skill
2. Run example prompts
3. Inspect the actual outputs
4. Add or refine assertions
5. Re-run after changes
6. Compare before vs after

## Human review

Use human review for subjective qualities such as:

- overall writing quality
- usefulness
- tone
- design taste
- whether the result feels like the right tradeoff

## What to ship

If the user asks for eval scaffolding, include:

- 5-10 prompts
- a mix of should-trigger and should-not-trigger prompts
- expected outputs
- simple assertions
- any unverified assumptions
