# Recipes

Source pages:

- `https://help.trmnl.com/en/articles/10122094-plugin-recipes`
- `https://help.trmnl.com/en/articles/10546870-compare-custom-plugin-types`

## When to recommend

Recommend a Recipe when:

- the plugin still fits the Private Plugin model
- the author wants a shareable TRMNL-native install path
- the author does not want to host user data on their own server

## Install vs fork

Install:

- simpler for less technical users
- receives upstream recipe updates automatically

Fork:

- editable like a private plugin
- does not receive updates from the original creator
- usually better for technical users who want to customize markup

## Publishing flow

1. Build a private plugin.
2. Publish it from the plugin settings page.
3. TRMNL reviews it for publication.

## Public vs unlisted

Public:

- visible from `/recipes` and `/plugins`
- moderated
- better discoverability

Unlisted:

- immediate share link
- skips moderation
- useful when the plugin is niche or does not meet public marketplace expectations

## Agent guidance

- Do not split Recipe logic into a separate build system. It is still a Private Plugin path.
- If the user wants a shareable artifact, add recipe publication notes after the private-plugin artifact pack.
