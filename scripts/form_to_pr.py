"""
form_to_pr.py — Parse a GitHub Issue Form submission and open a draft PR.

Usage:
  python scripts/form_to_pr.py new    /tmp/issue_body.txt
  python scripts/form_to_pr.py update /tmp/issue_body.txt

Environment variables required:
  ISSUE_NUMBER   GitHub issue number
  GH_TOKEN       GitHub token with contents/pull-requests/issues write access
  REPO           Repository in owner/name format (e.g. oarsi-biomech/resource-hub)
"""

import os
import re
import sys
import glob
import subprocess
import textwrap

import yaml


# ── Parsing ───────────────────────────────────────────────────────────────────

def parse_form_body(body):
    """Parse a GitHub Issue Form body into a {heading: value} dict."""
    result = {}
    # GitHub Issue Forms render each field as: ### Field Label\n\nvalue
    sections = re.split(r'\n###\s+', '\n' + body)
    for section in sections[1:]:
        lines = section.split('\n')
        key = lines[0].strip()
        value = '\n'.join(lines[1:]).strip()
        # Blank optional fields show as "_No response_"
        if value in ('_No response_', ''):
            value = ''
        # Strip checkbox markers from checklist answers
        value = re.sub(r'^- \[[xX ]\] ?', '', value, flags=re.MULTILINE).strip()
        result[key] = value
    return result


def parse_list_field(value):
    """Convert a newline-separated (possibly bullet-prefixed) value to a list."""
    lines = []
    for line in (value or '').split('\n'):
        line = re.sub(r'^[-*]\s+', '', line.strip())
        if line:
            lines.append(line)
    return lines


# ── Utilities ─────────────────────────────────────────────────────────────────

def to_kebab(s):
    """Convert a string to a kebab-case filename slug."""
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def normalize(s):
    """Normalize a string for fuzzy comparison (lowercase alphanumeric only)."""
    return re.sub(r'[^a-z0-9]', '', s.lower())


def fuzzy_match(a, b):
    """Return True if two strings are similar enough to flag as a duplicate."""
    na, nb = normalize(a), normalize(b)
    if not na or not nb or len(na) < 3 or len(nb) < 3:
        return False
    if na in nb or nb in na:
        return True
    shorter = na if len(na) <= len(nb) else nb
    longer = nb if len(na) <= len(nb) else na
    matches = sum(1 for c in shorter if c in longer)
    return matches / len(shorter) > 0.85


def bullet_list(items):
    """Render a Python list as a Markdown bullet list string."""
    return '\n'.join(f'- {item}' for item in items) if items else ''


def gh_comment(issue_number, body):
    """Post a comment on a GitHub issue via the gh CLI."""
    subprocess.run(
        ['gh', 'issue', 'comment', str(issue_number), '--body', body],
        check=True
    )


def gh_set_title(issue_number, title):
    """Update the title of a GitHub issue via the gh CLI."""
    subprocess.run(
        ['gh', 'issue', 'edit', str(issue_number), '--title', title],
        check=True
    )


def run(cmd, **kwargs):
    """Run a shell command, raising on failure."""
    return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, **kwargs)


# ── Duplicate detection ───────────────────────────────────────────────────────

def find_duplicates(lab_name, lead_pi, labs_dir='_labs'):
    """Search existing _labs/ entries for potential duplicates."""
    duplicates = []
    for filepath in glob.glob(f'{labs_dir}/*.md'):
        with open(filepath) as f:
            content = f.read()
        if not content.startswith('---'):
            continue
        try:
            end = content.index('---', 3)
            fm = yaml.safe_load(content[3:end]) or {}
        except Exception:
            continue
        existing_name = fm.get('title', '')
        existing_pi = fm.get('lead_investigators', '')
        if fuzzy_match(lab_name, existing_name) or fuzzy_match(lead_pi, existing_pi):
            duplicates.append({'file': filepath, 'name': existing_name, 'pi': existing_pi})
    return duplicates


# ── Entry builder ─────────────────────────────────────────────────────────────

def build_new_entry(fields):
    """Build a complete _labs/*.md file (front matter + markdown) from form fields."""
    name        = fields.get('Lab / Group / Center Name', '').strip()
    entry_type  = fields.get('Entry Type', '').strip()
    lead_pi     = fields.get('Lead Investigator(s) / Director(s)', '').strip()
    institution = fields.get('Institution', '').strip()
    city        = fields.get('City', '').strip()
    country     = fields.get('Country', '').strip()
    website     = fields.get('Website or Profile Link', '').strip()
    contact     = fields.get('Contact Method', '').strip()
    visitor     = fields.get('Openness to Visitors / Exchanges', '').strip()
    description = fields.get('Short Description', '').strip()
    focus_list  = parse_list_field(fields.get('OA / Biomechanics Focus Areas', ''))

    equipment      = parse_list_field(fields.get('Equipment / Methods (Optional)', ''))
    github_links   = parse_list_field(fields.get('GitHub / Code Links (Optional)', ''))
    datasets       = parse_list_field(fields.get('Open Datasets / Resources (Optional)', ''))
    affiliated     = parse_list_field(fields.get('Affiliated Centers / Resources (Optional)', ''))
    visitor_notes  = fields.get('Notes for Visitors / Trainees (Optional)', '').strip()
    collab         = parse_list_field(fields.get('Additional Collaboration Interests (Optional)', ''))

    fm_data = {
        'title': name,
        'entry_type': entry_type,
        'lead_investigators': lead_pi,
        'institution': institution,
        'city': city,
        'country': country,
        'visitor_exchange_openness': visitor,
        'focus_areas': focus_list,
    }
    fm_str = yaml.dump(fm_data, default_flow_style=False, allow_unicode=True).strip()

    parts = [
        f'---\n{fm_str}\n---\n',
        f'# {name}\n',
        '## Entry metadata\n',
        f'- **Name:** {name}',
        f'- **Entry type:** {entry_type}',
        f'- **Lead investigator(s) / director(s):** {lead_pi}',
        f'- **Institution:** {institution}',
        f'- **City:** {city}',
        f'- **Country:** {country}',
        f'- **Website or profile link:** {website}',
        f'- **Contact method:** {contact}',
        f'- **Visitor/exchange openness:** {visitor}\n',
        '## Short description\n',
        description + '\n',
        '## OA / biomechanics focus areas\n',
        bullet_list(focus_list) + '\n',
    ]

    if equipment:
        parts += ['### Equipment / methods\n', bullet_list(equipment) + '\n']
    if github_links:
        parts += ['### GitHub / code links\n', bullet_list(github_links) + '\n']
    if datasets:
        parts += ['### Open datasets / resources\n', bullet_list(datasets) + '\n']
    if affiliated:
        parts += ['### Affiliated centers / resources\n', bullet_list(affiliated) + '\n']
    if visitor_notes:
        parts += ['### Notes for visitors / trainees\n', visitor_notes + '\n']
    if collab:
        parts += ['### Additional collaboration interests\n', bullet_list(collab) + '\n']

    return '\n'.join(parts)


# ── Entry updater ─────────────────────────────────────────────────────────────

def find_entry_file(lab_name, lead_pi, labs_dir='_labs'):
    """Find the _labs/*.md file matching the given lab name and/or PI name."""
    for filepath in glob.glob(f'{labs_dir}/*.md'):
        with open(filepath) as f:
            content = f.read()
        if not content.startswith('---'):
            continue
        try:
            end = content.index('---', 3)
            fm = yaml.safe_load(content[3:end]) or {}
        except Exception:
            continue
        if fuzzy_match(lab_name, fm.get('title', '')) and fuzzy_match(lead_pi, fm.get('lead_investigators', '')):
            return filepath
    return None


def replace_section(content, heading, new_body):
    """Replace the content of a markdown section (between headings)."""
    # Find the section heading
    pattern = re.compile(
        r'(^#{1,3}\s+' + re.escape(heading.lstrip('#').strip()) + r'\s*\n)'
        r'(.*?)'
        r'(?=^#{1,3}\s|\Z)',
        re.MULTILINE | re.DOTALL
    )
    replacement = r'\1\n' + new_body.strip() + '\n\n'
    updated, count = pattern.subn(replacement, content)
    if count == 0:
        # Section doesn't exist — append it
        updated = content.rstrip('\n') + f'\n\n{heading}\n\n{new_body.strip()}\n'
    return updated


def apply_update(filepath, fields):
    """Apply non-blank update fields to an existing entry file."""
    with open(filepath) as f:
        content = f.read()

    # Parse existing front matter
    end = content.index('---', 3)
    fm = yaml.safe_load(content[3:end]) or {}

    # ── Update front matter fields ──
    fm_map = {
        'New Lab / Group / Center Name (if changing)':          'title',
        'New Lead Investigator(s) / Director(s) (if changing)': 'lead_investigators',
        'Institution (if changing)':                            'institution',
        'City (if changing)':                                   'city',
        'Country (if changing)':                                'country',
        'Website or Profile Link (if changing)':                'website',
        'Contact Method (if changing)':                         'contact',
    }
    for form_key, fm_key in fm_map.items():
        val = fields.get(form_key, '').strip()
        if val:
            fm[fm_key] = val

    for dropdown_key, fm_key in [
        ('Entry Type (if changing)', 'entry_type'),
        ('Openness to Visitors / Exchanges (if changing)', 'visitor_exchange_openness'),
    ]:
        val = fields.get(dropdown_key, '').strip()
        if val and val != '— no change —':
            fm[fm_key] = val

    focus_raw = fields.get('OA / Biomechanics Focus Areas (if changing)', '').strip()
    if focus_raw:
        fm['focus_areas'] = parse_list_field(focus_raw)

    # Write updated front matter back
    fm_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
    content = f'---\n{fm_str}\n---\n' + content[end + 3:]

    # ── Update markdown sections ──
    section_map = [
        ('Short Description (if changing)',                      '## Short description'),
        ('OA / Biomechanics Focus Areas (if changing)',         '## OA / biomechanics focus areas'),
        ('Equipment / Methods (if changing)',                    '### Equipment / methods'),
        ('GitHub / Code Links (if changing)',                    '### GitHub / code links'),
        ('Open Datasets / Resources (if changing)',              '### Open datasets / resources'),
        ('Affiliated Centers / Resources (if changing)',         '### Affiliated centers / resources'),
        ('Notes for Visitors / Trainees (if changing)',          '### Notes for visitors / trainees'),
        ('Additional Collaboration Interests (if changing)',     '### Additional collaboration interests'),
    ]
    for form_key, heading in section_map:
        val = fields.get(form_key, '').strip()
        if not val:
            continue
        items = parse_list_field(val)
        new_body = bullet_list(items) if items and heading.startswith('###') else val
        content = replace_section(content, heading, new_body)

    with open(filepath, 'w') as f:
        f.write(content)


# ── Git + PR helpers ──────────────────────────────────────────────────────────

def create_branch_and_pr(branch, commit_msg, pr_title, pr_body, issue_number):
    """Create a branch, commit staged changes, push, and open a draft PR."""
    run(f'git checkout -b {branch}')
    run(f'git add -A')
    run(f'git commit -m "{commit_msg}"')
    run(f'git push origin {branch}')

    result = subprocess.run(
        ['gh', 'pr', 'create',
         '--title', pr_title,
         '--body', pr_body,
         '--base', 'main',
         '--draft'],
        capture_output=True, text=True, check=True
    )
    pr_url = result.stdout.strip()

    gh_comment(issue_number, (
        f"Thanks for your submission! A draft PR has been opened for maintainer review:\n\n"
        f"{pr_url}\n\n"
        f"A maintainer will review and merge it once everything looks good. "
        f"You can follow along in the PR if you have a GitHub account."
    ))
    return pr_url


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    mode = sys.argv[1]          # 'new' or 'update'
    body_file = sys.argv[2]     # path to file containing raw issue body

    issue_number = int(os.environ['ISSUE_NUMBER'])

    with open(body_file) as f:
        body = f.read()

    fields = parse_form_body(body)

    if mode == 'new':
        lab_name = fields.get('Lab / Group / Center Name', '').strip()
        lead_pi  = fields.get('Lead Investigator(s) / Director(s)', '').strip()

        if not lab_name:
            gh_comment(issue_number, (
                "⚠️ Could not parse the lab name from your submission. "
                "Please ensure the form was filled out correctly, or open a new issue."
            ))
            sys.exit(1)

        gh_set_title(issue_number, f'[New Entry]: {lab_name}')

        # Duplicate detection
        duplicates = find_duplicates(lab_name, lead_pi)
        if duplicates:
            dup_list = '\n'.join(
                f"- **{d['name']}** (lead: {d['pi']})" for d in duplicates
            )
            gh_comment(issue_number, textwrap.dedent(f"""\
                🔍 **Possible duplicate detected**

                Your submission may match an existing entry:

                {dup_list}

                If this is the same lab, please close this issue and use the \
[update entry form](https://github.com/{os.environ['REPO']}/issues/new?template=update-lab-entry.yml) instead.

                If this is a **different** lab, no action needed — a maintainer \
will review and proceed with your submission.
            """))
            # Don't exit — let the maintainer decide; still create the PR

        # Build and write the entry file
        slug = to_kebab(lab_name)
        filepath = f'_labs/{slug}.md'
        content = build_new_entry(fields)
        with open(filepath, 'w') as f:
            f.write(content)

        branch = f'new-entry-{issue_number}-{slug}'
        create_branch_and_pr(
            branch=branch,
            commit_msg=f'Add {lab_name} entry (from issue #{issue_number})',
            pr_title=f'New entry: {lab_name}',
            pr_body=(
                f'Closes #{issue_number}\n\n'
                f'Auto-generated from issue #{issue_number}.\n\n'
                f'**Please review:** check that all fields are correct and the entry '
                f'is relevant to OA biomechanics or closely related research before merging.'
            ),
            issue_number=issue_number,
        )

    elif mode == 'update':
        current_name = fields.get('Current Lab / Group / Center Name', '').strip()
        current_pi   = fields.get('Current Lead Investigator / Director Name', '').strip()

        gh_set_title(issue_number, f'[Update Entry]: {current_name}')

        filepath = find_entry_file(current_name, current_pi)
        if not filepath:
            gh_comment(issue_number, textwrap.dedent(f"""\
                ⚠️ **Entry not found**

                We couldn't find an entry matching:
                - Lab name: **{current_name}**
                - Lead investigator: **{current_pi}**

                Please check the [directory](\
https://oarsi-biomech.github.io/resource-hub/labs/) to confirm the exact name \
as it appears, then close this issue and open a new update request with the \
corrected name.
            """))
            sys.exit(1)

        apply_update(filepath, fields)

        slug = to_kebab(current_name)
        branch = f'update-entry-{issue_number}-{slug}'
        display_name = fields.get('New Lab / Group / Center Name (if changing)', '').strip() or current_name

        create_branch_and_pr(
            branch=branch,
            commit_msg=f'Update {display_name} entry (from issue #{issue_number})',
            pr_title=f'Update entry: {display_name}',
            pr_body=(
                f'Closes #{issue_number}\n\n'
                f'Auto-generated update from issue #{issue_number}.\n\n'
                f'**Please review the diff** to confirm only intended fields were changed.'
            ),
            issue_number=issue_number,
        )


if __name__ == '__main__':
    main()
