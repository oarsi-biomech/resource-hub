# OARSI Biomechanics Resource Hub

The **OARSI Biomechanics Resource Hub** is a community-driven, GitHub Pages-compatible directory for osteoarthritis (OA) biomechanics and closely related human movement research groups.

Version 1 (v1) focuses on one core use case:

- A curated directory of labs, groups, and centers.

Future versions may expand to include shared code, datasets, and broader resources.

## v1 scope

### In scope
- Public GitHub Pages site structure.
- A directory of OA biomechanics-relevant labs/groups/centers.
- Simple contribution workflow for users with limited GitHub experience.
- Flexible file structure that can grow over time.

### Out of scope (v1)
- Shared dataset hosting.
- Shared code hosting.
- Advanced search/filtering.
- Maps.
- Automated metadata standardization.
- Complex affiliation logic.

## Repository structure

```text
.
├── index.md
├── labs/
│   ├── index.md
│   └── *.md
├── templates/
│   └── lab-entry-template.md
├── CONTRIBUTING.md
├── MAINTAINERS.md
└── .github/
    ├── CODEOWNERS
    └── PULL_REQUEST_TEMPLATE.md
```

## Content model (v1)

- **One page = one lab, group, or center**.
- Each entry lives in `labs/` as a Markdown file.
- The directory index is `labs/index.md`.

## Required fields per entry

- Name
- Entry type (lab, group, or center)
- Lead investigator(s) / director(s)
- Institution
- City
- Country
- Short description
- OA / biomechanics focus areas
- Website or profile link
- Contact method
- Visitor/exchange openness (yes, maybe, no)

## Optional fields per entry

- Equipment / methods
- GitHub / code links
- Open datasets / resources
- Affiliated centers / resources
- Notes for visitors / trainees
- Additional collaboration interests

> Rendering rule for v1: optional sections should be omitted when empty (do not leave blank headings).

## Getting started

1. Visit the homepage: `index.md`
2. Browse entries in `labs/index.md`
3. Add a new entry using `templates/lab-entry-template.md`
4. Open a pull request using the provided PR template.

See `CONTRIBUTING.md` for step-by-step instructions.
