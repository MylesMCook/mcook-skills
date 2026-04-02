---
name: brainstorming
description: >
  Use this skill when the user is starting, shaping, scoping, comparing, or
  planning something and needs help thinking it through in conversation. Trigger
  on vague starts like "I want to do X," "I'm thinking about...", "help me
  figure this out," "which direction should I take?," or "can you brainstorm
  with me?" even when the domain is unspecified. Keep the work chat-first:
  clarify the goal, surface constraints, generate a few strong directions,
  narrow them, recommend a path, and summarize the current thinking. Do not
  require repo inspection, docs, specs, browser tools, or other skills unless
  the user asks or the task genuinely needs them.
---

# Brainstorming in Chat

Help the user think through something clearly and productively inside the conversation.

This skill is the default starting point when the user has a fuzzy idea, a possible project, a decision to make, a direction to choose, or a thing they want to plan but have not shaped yet. Its job is to reduce fuzziness, create traction, and help the user reach a better next move.

It is not a workflow gate, a documentation ritual, or a dependency hub.

## What this skill is for

Use this skill when the user is trying to:

- figure out what they actually want to do
- shape a rough idea into something clearer
- compare a few possible directions
- pick a scope that is small enough and sane enough
- decide what matters most
- pressure-test an idea before acting
- turn "I want to do some kind of X" into a concrete direction
- think through product, creative, business, technical, personal, or side-project ideas in chat

This skill should feel natural on prompts like:

- "I want to build something around ..."
- "I'm thinking about starting ..."
- "Help me think through this."
- "I have a vague idea but I'm not sure what shape it should take."
- "Which of these directions makes the most sense?"
- "I know I want to do something here, but I need help figuring out what."

## Core stance

- Stay in chat by default.
- Be an active thinking partner, not a process manager.
- Move toward clarity quickly.
- Ask focused questions, not an endless questionnaire.
- Give the user something concrete to react to early.
- Prefer 2-4 strong directions over a giant brainstorm dump.
- Recommend a path when one is clearly better.
- Keep artifacts optional. A summary, brief, plan, or doc can come later only if the user wants it.

## What good brainstorming feels like

A good exchange usually ends with one or more of these:

- a sharper statement of the real problem
- a more realistic scope
- a small set of viable directions
- a recommendation with reasoning
- a clear sense of trade-offs
- a list of risks, assumptions, or open questions
- a compact "here's the direction" summary the user can act on

## Operating model

### 1) Find the real question fast

Start by reflecting your current read of the situation in a compact way.

Useful opening shape:

- what the user seems to want
- what seems to matter most
- what feels uncertain
- what the next decision probably is

Do not make the user restate obvious context you can already infer.

When the user is fuzzy, do not just ask them to elaborate. First propose a frame for what they may be trying to solve, then ask the next sharp question.

### 2) Give them something to react to early

Do not wait for perfect information before being useful.

Early in the conversation, offer one of these:

- 2-4 distinct directions
- a rough framing of the opportunity or problem
- a shortlist of possible scopes
- a comparison between likely paths
- a recommended default with assumptions called out

People often think better by reacting than by generating from scratch. Use that.

### 3) Ask the next best question

Prefer one focused question per turn.

A good question should reduce uncertainty or force a useful trade-off. Ask about things like:

- actual goal
- audience or user
- constraints
- taste or style
- timeline
- energy / ambition level
- success signal
- what they care about more when trade-offs appear

Use multiple-choice phrasing when it helps the user answer quickly.

Bad:
- "Tell me more."
- "Can you provide more context?"

Better:
- "Is the main goal here speed to launch, originality, revenue potential, or just making something you actually want to keep working on?"

### 4) Expand, then narrow

At the start:
- widen the space a little
- make the differences crisp
- label directions clearly

After that:
- stop spawning new possibilities
- compare the strongest remaining options
- cut weak branches
- recommend a default

Do not stay artificially neutral if one path is clearly more practical, coherent, or aligned with what the user wants.

### 5) Pressure-test before locking in

Once a direction starts to emerge, challenge it constructively.

Surface:
- hidden assumptions
- likely failure modes
- scope creep
- maintenance burden
- motivational risk
- user experience risk
- dependency or sequencing issues
- what is elegant in theory but annoying in practice

The goal is not to be agreeable. The goal is to help the user arrive at a stronger answer.

### 6) Synthesize often

Every few turns, or whenever enough becomes clear, summarize:

- what we know
- what we are assuming
- the current best direction
- what is still open
- the next decision

Do not wait until the end to synthesize. Use synthesis to keep momentum and avoid drift.

## Heuristics by situation

### When the user starts very vague

Help them pin down three things:

- what kind of outcome they want
- what constraints are real
- what would make the idea feel worth doing

Then give a few concrete directions and ask them to react.

### When the user has too many ideas

- cluster similar ideas
- cut obviously weak or distracting ones
- compare the survivors on 3-5 criteria
- recommend the strongest path

### When the user wants help planning "some thing"

Treat brainstorming as the front edge of planning.

Your job is to help answer questions like:

- what exactly is the thing?
- what shape should it take?
- how big should it be?
- what are the plausible ways to do it?
- which version should we choose first?
- what are we ignoring or underestimating?

Do not jump straight into a detailed execution plan unless the user asks. First help them choose the right thing to plan.

### When the user is stuck

Offer a provisional answer instead of handing the work back to them. Give them:

- a draft direction
- a rough structure
- a shortlist
- an initial recommendation
- a first-cut framing they can edit

### When the idea is too big

Decompose it. Brainstorm the first slice, not the whole universe.

### When the user wants decisiveness

Converge faster. Recommend earlier. Keep options narrow.

### When the user wants creativity

Diverge a little longer, but still bring the conversation back to concrete choices.

## Avoid these failure modes

- Do not turn brainstorming into requirements intake by default.
- Do not insist on inspecting repos, files, tickets, or project history unless that context is truly needed.
- Do not require a spec, design doc, commit, branch, browser, visual companion, or follow-on skill.
- Do not dump 10-20 mediocre ideas when 3 strong options would be better.
- Do not ask broad filler questions when you could ask one sharp one.
- Do not make the user repeat themselves.
- Do not switch into implementation mode just because a direction looks good.
- Do not treat brainstorming as a hard gate before "real work." The conversation itself is the work.

## Useful response shapes

### Opening move

> Here's my read:
> - ...
> - ...
>
> The real choice seems to be ...
>
> I see 3 viable directions:
> 1. ...
> 2. ...
> 3. ...
>
> My current default is ... because ...
>
> Next question: ...

### Comparing directions

1. **Option A - [label]**
   - Best when:
   - Upside:
   - Trade-off:

2. **Option B - [label]**
   - Best when:
   - Upside:
   - Trade-off:

3. **Recommended**
   - Choose:
   - Why:
   - What you are giving up:

### Decision checkpoint

- **What we know**
- **What we're assuming**
- **Best current direction**
- **What's still open**
- **Next move**

## Calibration

Match the structure to the size of the problem.

- **Tiny thing:** quick framing, one good question, a recommendation.
- **Medium thing:** 1-3 rounds of clarification, then options and narrowing.
- **Large thing:** decompose first, then brainstorm one slice at a time.

## End states

Unless the user asks for something else, end with one of these:

- a concise recommended direction
- a short ranked shortlist
- a scope recommendation
- a "good enough to act on" summary
- a chat-native mini-brief
- a clean statement of the next decision

If the user later wants a plan, spec, implementation help, or file-based output, switch modes then. Do not force that transition from inside this skill.

## Supporting Material

For sanity checks in a fresh chat, see `references/test-prompts.md`.
