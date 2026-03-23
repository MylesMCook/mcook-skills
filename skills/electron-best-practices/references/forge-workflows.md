# Forge Workflows

Use this file for Forge-first project setup and release planning.

## Default Recommendation For New Apps

- Start with Electron Forge.
- Prefer TypeScript.
- Prefer a preload-based architecture from the first commit.
- Prefer Vite when the app wants a modern web frontend stack and the project is not already on Webpack.

## Build Tool Choice

### Prefer Vite when

- the app is new
- the renderer is modern frontend code
- fast iteration matters
- the team is comfortable with Vite conventions

### Stay with Webpack when

- the project already uses the Forge Webpack plugin
- the current build is stable and migration does not solve a real problem
- existing loaders or plugin behavior are tightly coupled to Webpack

## TypeScript Stance

- Use TypeScript for new main, preload, and renderer code unless the project deliberately chose otherwise.
- Keep shared types small and explicitly owned.
- Use typed IPC contracts where possible so preload and renderer stay aligned.

## Packaging And Distribution

- Use Forge makers for platform installers and archives.
- Choose makers based on actual target platforms, not all possible formats by default.
- Decide signing, notarization, and release hosting early if the app is production-bound.
- Treat update strategy as part of packaging design, not as a last-step patch.

## Debugging And Operations

- Use Forge docs for exact debugging commands and plugin-specific behavior.
- Separate local developer ergonomics from production packaging concerns.
- Keep update code, release metadata, and platform packaging decisions in one reviewed path.

## Update Planning

- Confirm whether the app needs auto updates before selecting release infrastructure.
- Match update hosting and packaging strategy to the actual deployment channel.
- Verify platform-specific prerequisites in the official Electron and Forge docs before implementing updater code.

## When To Open Official Docs

- Open Forge getting started for current scaffolding guidance.
- Open the TypeScript guide before modifying TS support.
- Open Vite or Webpack plugin docs for exact config shape.
- Open makers and publishers docs for current packaging and release syntax.
