# OARSI Biomechanics Resource Hub

The **OARSI Biomechanics Resource Hub** is a community-driven directory for osteoarthritis biomechanics and related human movement research.

It is designed to help researchers discover labs, connect with collaborators, and explore shared resources across the field.

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

## What this includes (v1)

- A directory of labs, groups, and centers in OA biomechanics and related fields  
- Basic information about research focus, methods, and collaboration opportunities  
- Links to external websites, GitHub repositories, and resources where available  

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

- Each entry corresponds to one lab, group, or center.
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

> Note: Entries do not need to be perfectly formatted when submitted. Optional sections and placeholders can be left as-is; maintainers may clean or standardize entries when preparing the site.

## Contributing

We welcome contributions from the community.

You can add a new lab, group, or center, or update an existing entry.  
The process is designed to be simple and accessible, even for users with limited GitHub experience.

## Getting started

1. Visit the homepage: `index.md`
2. Browse entries in `labs/index.md`
3. Add a new entry using `templates/lab-entry-template.md`
4. Open a pull request using the provided PR template.

See `CONTRIBUTING.md` for step-by-step instructions.
