# Project Integration

## Goal

Every aircraft or STC project repo should consume shared certification knowledge without duplicating it.

## Recommended Reference Pattern

Use one of these patterns:

### Option 1: Git Submodule

Add this repo to each project repo under a predictable path such as `shared/certification`.

Why this is strong:

- Projects can pin to a known commit.
- Updates are explicit and reviewable.
- Shared knowledge stays centralized.

### Option 2: Sibling Repo Checkout

Keep the certification repo next to project repos on disk and reference it by relative path in tooling.

Why this is acceptable:

- Simpler for internal use.
- Easier during early adoption.

Risk:

- Weaker version pinning unless you explicitly record the commit.

## Project Repo Minimum Contract

Each project repo should contain a manifest based on `catalog/project-cert-manifest-template.yaml`.

That manifest should identify:

- the version of the shared certification repo
- the governing guidance records
- the adopted compliance positions
- the report templates being used
- any approved project-specific deviations

## Example Report-Building Flow

1. Project repo declares the manifest.
2. Team runs the selector utility to propose initial compliance position IDs for that manifest.
3. Report tooling reads the manifest.
4. Tooling pulls approved source summaries, positions, and templates from the shared repo.
5. Tooling combines those with project evidence and findings.
6. Final report cites both governing sources and project-specific substantiation.

## What This Prevents

- Teams copying stale guidance into project repos.
- Different projects using conflicting interpretations.
- Report language drifting away from approved positions.
- Rebuilding the same certification logic from scratch on every project.