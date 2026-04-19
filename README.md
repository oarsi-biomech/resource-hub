# OARSI Biomechanics Resource Hub

The **OARSI Biomechanics Resource Hub** is a community-driven directory for osteoarthritis biomechanics and related human movement research.

It is designed to help researchers discover labs, connect with collaborators, and explore shared resources across the field.

Version 1 (v1) focuses on one core use case:

- A curated directory of labs, groups, and centers.

Future versions may expand to include shared code, datasets, and broader resources.

This is a growing, community-contributed resource — new labs are added regularly.

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
├── _labs/
│   └── *.md          # lab/group/center entries (Jekyll collection)
├── labs/
│   └── index.md      # auto-generated directory listing
├── _config.yml       # Jekyll configuration
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
2. Browse entries in the `labs/` directory
3. Add a new entry using `templates/lab-entry-template.md`
4. Open a pull request using the provided PR template.

See `CONTRIBUTING.md` for step-by-step instructions.

## Local preview

Run the site locally (matches what GitHub Pages will render) to review changes before merging a pull request.

Instructions below are for macOS. If something fails, the [Troubleshooting](#local-preview-troubleshooting) section at the bottom covers every issue we've hit so far.

### One-time setup

Open Terminal (⌘ + space, type "Terminal") and run the steps below.

**1. Install Homebrew** (skip if you already have it — run `brew --version` to check):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2. Install the Xcode Command Line Tools** (skip if `xcode-select -p` prints a path):

```bash
xcode-select --install
```

A GUI dialog appears — click "Install" and wait for it to finish (~5–10 min).

**3. Install rbenv and Ruby 3.3.6** (rbenv lets you run a newer Ruby than macOS ships with):

```bash
brew install rbenv ruby-build
```

Then wire rbenv into your shell so new terminals use it automatically:

```bash
echo '
# rbenv
eval "$(rbenv init - --no-rehash zsh)"' >> ~/.zshrc
```

Also add this line so native gems can find macOS system headers (avoids a common build error — see troubleshooting below):

```bash
echo '
# macOS SDK for native gem builds
export SDKROOT=$(xcrun --show-sdk-path)' >> ~/.zshrc
```

**Close the Terminal window and open a new one** (shell config only takes effect in new sessions). Then:

```bash
rbenv install 3.3.6
```

This takes a few minutes. Verify:

```bash
ruby -v                   # should print: ruby 3.3.6...
```

**4. Clone the repo and install site dependencies:**

```bash
git clone https://github.com/oarsi-biomech/resource-hub.git
cd resource-hub
bundle install
```

The repo's `.ruby-version` file tells rbenv to use 3.3.6 automatically. `bundle install` generates `Gemfile.lock` — commit it the first time it's created.

### Run the site

From inside the repo:

```bash
bundle exec jekyll serve --livereload
```

Open http://localhost:4000. Edits to markdown files rebuild automatically; the browser reloads.

Stop the server with `Ctrl + C`.

### Preview a pull request

With the [GitHub CLI](https://cli.github.com/) (`brew install gh`, then `gh auth login`):

```bash
gh pr checkout <number>             # e.g. gh pr checkout 12
bundle exec jekyll serve --livereload
```

Without `gh`:

```bash
git fetch origin pull/<number>/head:pr-<number>
git checkout pr-<number>
bundle exec jekyll serve --livereload
```

When finished reviewing, stop the server (`Ctrl + C`) and switch back to main:

```bash
git checkout main
```

<a id="local-preview-troubleshooting"></a>

### Troubleshooting

<details>
<summary><strong><code>bundle install</code> says "ruby 2.6.10 is incompatible"</strong></summary>

Your terminal is using macOS system Ruby instead of the rbenv version. This happens when `rbenv init` isn't loaded in the current shell. Confirm the fix is in your config:

```bash
grep "rbenv init" ~/.zshrc
```

If nothing prints, rerun the `echo ... >> ~/.zshrc` command from step 3, then **open a new terminal window** (sourcing isn't enough — open a fresh one). Verify with `ruby -v`; it should print 3.3.6.
</details>

<details>
<summary><strong>eventmachine fails to install with <code>'iostream' file not found</code></strong></summary>

`SDKROOT` isn't set, so the C++ compiler can't find macOS system headers. Confirm:

```bash
echo $SDKROOT                       # should print a path ending in .sdk
```

If empty, rerun the `echo ... SDKROOT ... >> ~/.zshrc` command from step 3, then open a new terminal and retry `bundle install`.
</details>

<details>
<summary><strong>eventmachine fails with <code>CXX = false</code> or "make: *** [binder.o] Error 1"</strong></summary>

Ruby was built before Command Line Tools were installed, so it recorded the C++ compiler as `false`. Fix by rebuilding Ruby:

```bash
rbenv uninstall 3.3.6
rbenv install 3.3.6
bundle install
```
</details>

<details>
<summary><strong>eventmachine fails with <code>openssl</code> errors</strong></summary>

Tell the build where Homebrew's OpenSSL headers live:

```bash
bundle config build.eventmachine --with-cppflags=-I/opt/homebrew/opt/openssl@3/include
bundle install
```

If OpenSSL isn't installed: `brew install openssl@3`.
</details>

<details>
<summary><strong>Port 4000 is already in use</strong></summary>

Either another Jekyll server is still running (find it with `lsof -i :4000` and kill it), or use a different port:

```bash
bundle exec jekyll serve --livereload --port 4001
```
</details>
