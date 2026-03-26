# Advanced Third Party Plugins

Source pages:

- `https://docs.trmnl.com/go/plugin-marketplace/introduction`
- `https://docs.trmnl.com/go/plugin-marketplace/plugin-creation`
- `https://docs.trmnl.com/go/plugin-marketplace/plugin-installation-flow`
- `https://docs.trmnl.com/go/plugin-marketplace/plugin-management-flow`
- `https://docs.trmnl.com/go/plugin-marketplace/plugin-screen-generation-flow`

## Escalation rule

Only recommend this path if the request genuinely needs:

- OAuth with the author's application
- user identity or email on the author's server
- a custom management UI outside TRMNL
- a public marketplace integration backed by the author's own service

## Required plugin definition fields

TRMNL asks for:

- `name`
- `description`
- `icon`
- `installation_url`
- `installation_success_webhook_url`
- `plugin_management_url`
- `plugin_markup_url`
- `uninstallation_webhook_url`

## Install flow

1. TRMNL sends an installation request to `installation_url` with a one-time token and callback URL.
2. The author's server exchanges that token for an access token at `https://trmnl.com/oauth/token`.
3. The author redirects the user back to TRMNL through the installation callback URL.
4. TRMNL sends a success webhook containing user details and plugin setting identifiers.

## Management flow

- TRMNL redirects the user to `plugin_management_url?uuid=<plugin-connection-uuid>`.
- The UUID identifies that specific installed plugin instance.
- Returning to TRMNL with `?force_refresh=true` triggers screen generation on the user's behalf.

## Screen generation flow

- TRMNL POSTs to `plugin_markup_url`.
- The request includes `user_uuid` and a `trmnl` metadata object.
- Authorization is provided as a Bearer token.
- The response should include markup nodes for every supported layout.

## Agent guidance

- Be explicit that this path needs an external server and code.
- If the user asked for "no code", explain why this path violates that requirement and propose a Private Plugin fallback if possible.
