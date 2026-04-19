# Signs of AI Writing

Use this file when the user asks to humanize text, remove AI style, make prose sound natural, or polish model-generated text. The goal is not to hide authorship; it is to remove generic filler and restore specific meaning.

## Core diagnosis

AI-sounding writing usually has three problems:

1. It inflates importance without adding facts.
2. It smooths specific claims into generic abstractions.
3. It uses polished transitions and formatting to imitate structure.

Fix the underlying problem. Do not merely swap words.

## Common patterns

### Puffy importance

Watch for:
- pivotal, vital, crucial, significant, transformative
- testament to, enduring legacy, profound impact
- plays a key role, serves as a reminder, underscores the importance

Fix by naming the actual effect.

Weak:
> The migration marks a pivotal step in improving system reliability.

Better:
> The migration moves session reads to Redis, reducing database load during login spikes.

### Empty “-ing” commentary

Watch for:
- ensuring reliability
- showcasing capabilities
- highlighting importance
- reflecting commitment
- empowering users
- driving innovation

Fix by stating the mechanism or deleting the phrase.

Weak:
> The dashboard adds filters, enabling teams to gain actionable insights.

Better:
> The dashboard lets teams filter incidents by service, severity, and owner.

### Promotional adjectives

Watch for:
- seamless
- robust
- cutting-edge
- innovative
- powerful
- world-class
- best-in-class

Fix by using measurable or observable claims.

Weak:
> A robust workflow for seamless collaboration.

Better:
> A review workflow that lets editors comment before publication.

### Generic transitions

Watch for:
- In today’s fast-paced landscape
- In conclusion
- Overall
- Furthermore / Moreover / Additionally overuse
- It is important to note
- When it comes to

Fix by moving directly to the point.

### Repetitive triads

AI prose often uses three-part lists for rhythm rather than meaning.

Weak:
> The tool is fast, flexible, and reliable.

Better:
> The tool processes 10,000 rows in under a minute.

### Fake balance

Watch for formulaic contrast:
- not only X but Y
- while X, it also Y
- despite these challenges
- however, it is important to note

Fix by stating the real relationship.

## Humanization pass

1. Identify the real claim in each sentence.
2. Delete sentences that only praise, transition, or summarize.
3. Replace abstractions with concrete nouns and verbs.
4. Keep the user’s intent and level of formality.
5. Vary sentence length naturally.
6. Remove decorative bolding, emoji, and excessive bullets unless the user asked for them.
7. End with the action, decision, or strongest useful detail.

## Word watchlist

These words are not banned. They require a reason:

`align`, `delve`, `elevate`, `enhance`, `foster`, `garner`, `holistic`, `impactful`, `innovative`, `interplay`, `intricate`, `landscape`, `leverage`, `multifaceted`, `nuanced`, `pivotal`, `realm`, `robust`, `seamless`, `showcase`, `streamline`, `tapestry`, `testament`, `transformative`, `underscore`, `unlock`, `vibrant`, `vital`.

## Good final test

Read the text aloud. If it sounds like a brochure, a grant application, or a generic LinkedIn post, cut another layer and add a specific fact.
