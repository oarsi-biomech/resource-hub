# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

The **OARSI Biomechanics Resource Hub** is a Markdown-first, static content repository — not an application codebase. There is no build pipeline, no package manager, and no test runner. All content is plain Markdown intended for GitHub Pages-style rendering.

v1 scope is intentionally constrained: a curated directory of OA biomechanics labs/groups/centers. No dataset hosting, code hosting, maps, advanced search, or automation.

## Architecture

```
index.md                          # Site entry point
_config.yml                       # Jekyll configuration (defines labs collection)
_labs/
  <descriptive-kebab-case>.md     # One file per lab/group/center entry (Jekyll collection)
labs/
  index.md                        # Auto-generated directory listing (Liquid template)
templates/
  lab-entry-template.md           # Canonical schema for new entries (includes YAML front matter)
.github/
  PULL_REQUEST_TEMPLATE.md
  CODEOWNERS
  ISSUE_TEMPLATE/                 # Structured contribution forms (Issues #4 and #5)
```

Entries live in `_labs/` as a Jekyll collection. Each entry has YAML front matter at the top (title, entry_type, lead_investigators, institution, city, country, visitor_exchange_openness, focus_areas) followed by the full Markdown content. `labs/index.md` auto-generates the listing via Liquid — do not edit it manually to add entries.

## Content model

New entries must include: Name, Entry type (lab/group/center), Lead investigator(s), Institution, City, Country, Website/profile link, Contact method, Visitor/exchange openness (yes/maybe/no), Short description, OA/biomechanics focus areas.

Optional sections: Equipment/methods, GitHub/code links, Open datasets/resources, Affiliated centers, Notes for visitors/trainees, Collaboration interests. Optional sections may be left with placeholder text — contributors are not required to delete empty headings. Maintainers clean up unused sections when preparing entries. This "messy input → clean output" approach was chosen deliberately to lower the contribution barrier.

The canonical field structure lives in `templates/lab-entry-template.md`. Always match heading order and naming to that template unless explicitly changing the schema.

## Conventions

- New entry filenames: `_labs/<descriptive-kebab-case>.md`
- Internal repo links: relative paths. External links: full URLs.
- Descriptions: concise, plain language — not promotional.
- When editing an entry: touch only that entry and `labs/index.md` if needed. Do not reformat unrelated content.
- When changing the schema: update `README.md`, `CONTRIBUTING.md`, `templates/lab-entry-template.md`, and any index pages together in the same PR.
- License: MIT — chosen intentionally so content can be freely reused by the community.

## Contribution workflow

Two parallel paths for submitting or updating entries:

**Path 1 — GitHub Issue Forms (primary path for non-GitHub users)**
- `new-lab-entry` form (`.github/ISSUE_TEMPLATE/new-lab-entry.yml`): structured web form with all required and optional fields. Includes a soft-dedup checkbox ("I searched the directory and my lab is not already listed"). A GitHub Action auto-creates a formatted draft PR from the submission.
- `update-lab-entry` form (`.github/ISSUE_TEMPLATE/update-lab-entry.yml`): identifies the entry by both lab name AND lead investigator/director name (needed because many biomechanics labs share generic acronym-style names like MOBL/WOBL). All fields are updatable including lab name and director name. A GitHub Action finds the correct file and opens a draft PR.
- Duplicate detection: when a `new-lab-entry` issue is opened, an Action fuzzy-matches the submitted lab name and lead investigator name against existing `_labs/` entries and comments if a potential duplicate is found — matching on both fields prevents false positives from shared acronyms.

**Path 2 — Direct PR (for GitHub-comfortable contributors)**
- Fork → edit/create a file in `labs/` (or `_labs/` after Jekyll migration) → open PR using the PR template.

Issue Forms always display all optional fields, so structure is preserved regardless of what contributors fill in. For direct-file edits, `templates/lab-entry-template.md` is the authoritative source; link to it prominently in CONTRIBUTING.md.

## PR expectations

PR descriptions should cover: what changed, why it changed, and any follow-up needed by maintainers. Use the PR template in `.github/PULL_REQUEST_TEMPLATE.md`. Structural changes (template, governance, folder layout) prefer two maintainer approvals; normal changes need one.

## GitHub Pages

The site is deployed via GitHub Pages from the `main` branch at root `/`.
Live URL: `https://oarsi-biomech.github.io/resource-hub/`

## Roadmap

The project follows a 4-phase plan established at inception:

- **Phase 1** (complete): Org/repo, lab template, CONTRIBUTING/MAINTAINERS docs, CODEOWNERS, seed lab entry, GitHub Pages enabled.
- **Phase 2**: Nicer index page, improved browsing and filtering.
- **Phase 3**: Optional structured metadata, GitHub issue forms for submissions, and potentially a map or searchable directory.
- **Phase 4**: Links to shared code, datasets, and broader community resources.

### Issue execution order

The five open issues have dependencies — work through them in this sequence:

| Order | Issue | Depends on |
|-------|-------|-----------|
| 1 | [#3 Jekyll `_labs/` collection migration](https://github.com/oarsi-biomech/resource-hub/issues/3) | nothing — do first, locks schema |
| 2 | [#4](https://github.com/oarsi-biomech/resource-hub/issues/4) + [#5](https://github.com/oarsi-biomech/resource-hub/issues/5) Issue Forms (one PR) | #3 schema |
| 3 | [#7 Client-side filtering](https://github.com/oarsi-biomech/resource-hub/issues/7) | #3 |
| 4 | [#6 Auto-PR GitHub Action](https://github.com/oarsi-biomech/resource-hub/issues/6) | #3 + #4 + #5 |

Update this file after each issue is closed to keep architecture notes current.

### Planned features by phase

**Phase 2 (next up):**
- Jekyll `_labs/` collection migration: move entries to `_labs/`, add `_config.yml`, add YAML front matter to each entry (title, entry_type, institution, city, country, visitor_exchange_openness), auto-generate directory listing. Tracked in GitHub issue. Branch: `issue-<N>-auto-generate-labs-directory`.
- GitHub Issue Forms for new and update submissions (Issues B and C) — enables non-GitHub contributor path and prevents structural loss.
- GitHub Action to auto-convert form submissions into formatted draft PRs, with duplicate detection on lab name + lead investigator name (Issue D). Depends on Jekyll migration.
- Client-side metadata filtering on the directory page: filter by country, visitor/exchange openness, and OA focus area. **Multi-select required** (e.g., visitor openness = "yes" OR "maybe" in one query). Vanilla JS, no external dependencies (Issue E).

**Phase 3:**
- Pagefind full-text search via GitHub Actions build step. Free for public repos (MIT licensed). Depends on Phase 2 Jekyll migration being complete.

**Phase 4:**
- Links to shared code, datasets, and broader community resources.

All tools in the plan (lunr.js, Pagefind, vanilla JS filtering, GitHub Actions) are free for public repositories.

## Validation (no automated linting)

Before proposing changes, manually confirm:
- Markdown headings are coherent and render correctly.
- Internal links resolve to existing files.
- New entry filenames follow kebab-case convention.
- `labs/index.md` is auto-generated — do not manually add entry links to it.
