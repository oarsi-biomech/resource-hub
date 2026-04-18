---
title: Labs / Groups / Centers Directory
layout: default
---

# Labs / Groups / Centers Directory

This directory lists labs, groups, and centers working in osteoarthritis biomechanics and related areas.

<div id="directory-app">

<div id="filter-panel" style="background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:1rem 1.25rem;margin-bottom:1.25rem;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
    <strong>Filter directory</strong>
    <button id="clear-filters" onclick="clearFilters()" style="font-size:0.85rem;padding:0.2rem 0.6rem;cursor:pointer;">Clear all</button>
  </div>
  <div id="filter-groups" style="display:flex;flex-wrap:wrap;gap:1.5rem;"></div>
</div>

<p id="entry-count" style="font-size:0.9rem;color:#57606a;margin-bottom:0.75rem;"></p>

<ul id="lab-list"></ul>

</div>

<p style="margin-top:2rem;">
  <strong>Want to add your lab?</strong> Use the <a href="https://github.com/oarsi-biomech/resource-hub/issues/new?template=new-lab-entry.yml">new lab entry form</a>.<br>
  <strong>Need to update an existing entry?</strong> Use the <a href="https://github.com/oarsi-biomech/resource-hub/issues/new?template=update-lab-entry.yml">update entry form</a>.
</p>

<!-- Lab data injected by Jekyll -->
<script id="labs-data" type="application/json">
[{% assign sorted_labs = site.labs | sort: 'title' %}{% for lab in sorted_labs %}
  {
    "title": {{ lab.title | jsonify }},
    "url": {{ lab.url | relative_url | jsonify }},
    "institution": {{ lab.institution | default: "" | jsonify }},
    "city": {{ lab.city | default: "" | jsonify }},
    "country": {{ lab.country | default: "" | jsonify }},
    "visitor_exchange_openness": {{ lab.visitor_exchange_openness | default: "" | jsonify }},
    "focus_areas": {{ lab.focus_areas | default: "" | jsonify }}
  }{% unless forloop.last %},{% endunless %}{% endfor %}
]
</script>

<script>
(function () {
  const labs = JSON.parse(document.getElementById('labs-data').textContent);

  // ── Filter state ────────────────────────────────────────────────────
  const filterState = {
    country: new Set(),
    visitor_exchange_openness: new Set(),
    focus_areas: new Set()
  };

  const filterMeta = [
    { key: 'country',                   label: 'Country' },
    { key: 'visitor_exchange_openness', label: 'Open to visitors' },
    { key: 'focus_areas',               label: 'Focus area' },
  ];

  // ── Collect unique values per dimension ─────────────────────────────
  function uniqueValues(key) {
    const vals = new Set();
    labs.forEach(lab => {
      const v = lab[key];
      if (Array.isArray(v)) v.forEach(x => x && vals.add(x));
      else if (v) vals.add(v);
    });
    return [...vals].sort();
  }

  // ── Build filter UI ──────────────────────────────────────────────────
  const filterGroups = document.getElementById('filter-groups');
  filterMeta.forEach(({ key, label }) => {
    const values = uniqueValues(key);
    if (!values.length) return;

    const group = document.createElement('div');
    group.style.cssText = 'min-width:160px;';

    const heading = document.createElement('div');
    heading.style.cssText = 'font-size:0.8rem;font-weight:600;text-transform:uppercase;letter-spacing:0.04em;color:#57606a;margin-bottom:0.4rem;';
    heading.textContent = label;
    group.appendChild(heading);

    values.forEach(val => {
      const wrapper = document.createElement('label');
      wrapper.style.cssText = 'display:flex;align-items:center;gap:0.35rem;font-size:0.9rem;cursor:pointer;margin-bottom:0.2rem;';

      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.value = val;
      cb.addEventListener('change', () => {
        cb.checked ? filterState[key].add(val) : filterState[key].delete(val);
        render();
      });

      wrapper.appendChild(cb);
      wrapper.appendChild(document.createTextNode(val));
      group.appendChild(wrapper);
    });

    filterGroups.appendChild(group);
  });

  // ── Filter logic ─────────────────────────────────────────────────────
  function labMatches(lab) {
    for (const { key } of filterMeta) {
      const active = filterState[key];
      if (!active.size) continue;
      const v = lab[key];
      const labVals = Array.isArray(v) ? v : (v ? [v] : []);
      if (!labVals.some(x => active.has(x))) return false;
    }
    return true;
  }

  // ── Render listing ───────────────────────────────────────────────────
  const list = document.getElementById('lab-list');
  const countEl = document.getElementById('entry-count');

  function render() {
    const visible = labs.filter(labMatches);
    countEl.textContent = 'Showing ' + visible.length + ' of ' + labs.length + ' entr' + (labs.length === 1 ? 'y' : 'ies');

    list.innerHTML = '';
    if (!visible.length) {
      const empty = document.createElement('li');
      empty.style.color = '#57606a';
      empty.textContent = 'No entries match the selected filters.';
      list.appendChild(empty);
      return;
    }

    visible.forEach(lab => {
      const visitorLabel = { yes: 'Open to visitors', maybe: 'Visitors: maybe', no: 'Closed to visitors' }[lab.visitor_exchange_openness] || '';
      const li = document.createElement('li');
      const link = document.createElement('a');
      link.href = lab.url;
      link.textContent = lab.title;
      li.appendChild(link);
      li.appendChild(document.createTextNode(' \u2014 ' + lab.institution + ', ' + lab.country));
      if (visitorLabel) {
        const em = document.createElement('em');
        em.style.cssText = 'color:#57606a;font-size:0.85rem;';
        em.textContent = ' (' + visitorLabel + ')';
        li.appendChild(em);
      }
      list.appendChild(li);
    });
  }

  // ── Clear all ────────────────────────────────────────────────────────
  window.clearFilters = function () {
    Object.values(filterState).forEach(s => s.clear());
    document.querySelectorAll('#filter-panel input[type=checkbox]').forEach(cb => { cb.checked = false; });
    render();
  };

  render();
})();
</script>
