# AGENTS.md

This file provides operating guidance for coding agents working in this repository.

## Repository purpose

The **OARSI Biomechanics Resource Hub** is a community-maintained, Markdown-first directory of osteoarthritis biomechanics labs, groups, and centers.

v1 is intentionally simple: static content, straightforward contribution flow, and maintainability over automation.

## Architecture overview

This repository is a **content architecture** (not an application codebase):

- **Site entry point**: `index.md`
- **Directory section**: `labs/`
  - `labs/index.md` is the section landing page
  - individual lab/group/center entries are one file each in `labs/*.md`
- **Authoring template**: `templates/lab-entry-template.md`
- **Process docs**:
  - `README.md` (scope + structure)
  - `CONTRIBUTING.md` (how to add/update entries)
  - `MAINTAINERS.md` (maintenance responsibilities)

There is no build pipeline enforced here; files should remain valid, readable Markdown suitable for GitHub Pages-style rendering.

## Content model (v1)

Each `labs/*.md` file represents one entity (lab/group/center).

### Required information

- Name
- Entry type (lab/group/center)
- Lead investigator(s) / director(s)
- Institution
- City
- Country
- Short description
- OA / biomechanics focus areas
- Website or profile link
- Contact method
- Visitor/exchange openness (yes/maybe/no)

### Optional information

- Equipment / methods
- GitHub / code links
- Open datasets / resources
- Affiliated centers / resources
- Notes for visitors / trainees
- Collaboration interests

## Authoring and editing conventions

When editing content, prioritize consistency and ease of community contribution:

1. Keep headings and section order aligned with `templates/lab-entry-template.md` unless maintainers explicitly change the schema.
2. Prefer concise, plain-language descriptions over promotional text.
3. Preserve contributor intent; only normalize formatting where needed for readability.
4. Use relative links for internal repository references and full URLs for external resources.
5. Avoid introducing new required fields without updating template + README/CONTRIBUTING docs.

## File placement rules

- New lab entries: `labs/<descriptive-kebab-case>.md`
- Do not place lab entries at repository root.
- Keep templates in `templates/` and avoid duplicating template content into multiple files unless necessary.

## Change management guidance for agents

Before making structural or schema changes:

- Update the relevant docs together (`README.md`, `CONTRIBUTING.md`, template, and any index pages).
- Keep v1 constraints in mind (no advanced search/maps/automation assumptions).
- Prefer incremental, review-friendly PRs.

For small content additions/edits:

- Touch only the specific entry and any required index links.
- Do not refactor unrelated formatting.

## Validation checklist

Agents should run lightweight checks before proposing changes:

- Markdown files render and headings are coherent.
- Internal links resolve to existing files.
- New entry filenames follow project naming style.

If no automated linting exists, document manual checks performed in the PR.

## Pull request expectations

PR descriptions should include:

- What changed
- Why it changed
- Any follow-up needed by maintainers

For schema/architecture updates, include a brief migration note for future contributors.
