# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

The **OARSI Biomechanics Resource Hub** is a Markdown-first, static content repository — not an application codebase. There is no build pipeline, no package manager, and no test runner. All content is plain Markdown intended for GitHub Pages-style rendering.

v1 scope is intentionally constrained: a curated directory of OA biomechanics labs/groups/centers. No dataset hosting, code hosting, maps, advanced search, or automation.

## Architecture

```
index.md                         # Site entry point
labs/
  index.md                       # Directory section landing page
  <descriptive-kebab-case>.md    # One file per lab/group/center entry
templates/
  lab-entry-template.md          # Canonical schema for new entries
.github/
  PULL_REQUEST_TEMPLATE.md
  CODEOWNERS
```

Each `labs/*.md` file is a self-contained entry. The `labs/index.md` must be kept in sync whenever entries are added or removed.

## Content model

New entries must include: Name, Entry type (lab/group/center), Lead investigator(s), Institution, City, Country, Website/profile link, Contact method, Visitor/exchange openness (yes/maybe/no), Short description, OA/biomechanics focus areas.

Optional sections: Equipment/methods, GitHub/code links, Open datasets/resources, Affiliated centers, Notes for visitors/trainees, Collaboration interests. Optional sections may be left with placeholder text — contributors are not required to delete empty headings. Maintainers clean up unused sections when preparing entries. This "messy input → clean output" approach was chosen deliberately to lower the contribution barrier.

The canonical field structure lives in `templates/lab-entry-template.md`. Always match heading order and naming to that template unless explicitly changing the schema.

## Conventions

- New entry filenames: `labs/<descriptive-kebab-case>.md`
- Internal repo links: relative paths. External links: full URLs.
- Descriptions: concise, plain language — not promotional.
- When editing an entry: touch only that entry and `labs/index.md` if needed. Do not reformat unrelated content.
- When changing the schema: update `README.md`, `CONTRIBUTING.md`, `templates/lab-entry-template.md`, and any index pages together in the same PR.
- License: MIT — chosen intentionally so content can be freely reused by the community.

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

### Immediate next planned feature: Jekyll auto-directory

The current `labs/index.md` is maintained manually — every new entry requires a second edit to add it to the listing. The plan is to migrate to a **Jekyll collection** to auto-generate the directory page:

- Move entries from `labs/` to `_labs/`
- Add `_config.yml` with the collection definition
- Add YAML front matter to each entry (title, entry_type, institution, city, country, visitor_exchange_openness)
- Rewrite `labs/index.md` to loop over the collection automatically

Track this via a GitHub issue and branch named `issue-<N>-auto-generate-labs-directory`. Until this migration happens, `labs/index.md` must still be updated manually when entries are added or removed.

### Future contribution path consideration

A non-GitHub submission route (e.g. Google Form that maintainers convert into PRs) has been noted as a future option for GitHub-naive contributors. Not in scope until the community grows.

## Validation (no automated linting)

Before proposing changes, manually confirm:
- Markdown headings are coherent and render correctly.
- Internal links resolve to existing files.
- New entry filenames follow kebab-case convention.
- `labs/index.md` reflects any added/removed entries (until Jekyll auto-directory is implemented).
