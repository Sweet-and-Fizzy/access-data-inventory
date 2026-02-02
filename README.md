# ACCESS Data Inventory

Unified documentation for ACCESS data sources, APIs, and MCP tools.

## How It Works

1. **Edit** a markdown file in `data-sources/`
2. **Commit** and push to `main`
3. **Done** - GitHub Actions regenerates all docs automatically

The generated documentation is published to:
- **GitHub Pages** - browsable docs and interactive relationship diagram
- **dbdocs.io** - interactive ERD at https://dbdocs.io/access-ci/access-data-inventory

## Adding or Editing a Data Source

Edit or create a `.md` file in `data-sources/`. Each file has YAML frontmatter for structured data and markdown for notes.

### Minimal Example

```markdown
---
id: my_source
name: My Data Source
description: What this source contains
category: Community & Outreach
track: Support
responsible_team: Support
access_level: Public
is_canonical: false
canonical_source: null
api_endpoint: null
priority: Medium

mcp:
  available: false
  package: null
  tools: []

fields: []
relationships: []
---

## Overview

Description of this data source.
```

### Full Example with Fields

```markdown
---
id: my_source
name: My Data Source
description: What this source contains
category: Community & Outreach
track: Support
responsible_team: Support
access_level: Public
is_canonical: false
canonical_source: access-support-drupal
api_endpoint: https://example.com/api
dynamic: false
priority: Medium

mcp:
  available: true
  package: "@access-mcp/my-source"
  tools:
    - name: search_my_source
      method: GET
      description: Search with filters

fields:
  - name: id
    type: int
    access: Public
    primary_key: true
    description: Unique identifier

  - name: title
    type: varchar
    access: Public
    required: true
    mcp_name: title
    description: Display title

  - name: internal_notes
    type: text
    access: Internal Only
    description: Staff-only notes

relationships:
  - type: belongs_to
    target: other_source
    field: other_id
    description: Links to other source

  - type: has_many
    target: tags
    through: entity_tags
    description: Tagged for categorization
---

## Overview

Detailed description of this data source.

## Notes

- Additional context
- Known issues or limitations
```

### Field Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Field name |
| `type` | Yes | `int`, `varchar`, `text`, `boolean`, `date`, `timestamp`, `decimal` |
| `access` | Yes | `Public`, `Authenticated`, `Restricted`, `Internal Only`, `Sensitive` |
| `description` | Yes | What this field contains |
| `primary_key` | No | Set `true` for primary key |
| `required` | No | Set `true` if field is required |
| `mcp_name` | No | Field name in MCP if different |
| `computed` | No | Set `true` if calculated/derived |
| `references` | No | Foreign key reference (e.g., `users.user_id`) |
| `allowed_values` | No | List of valid values |

### Allowed Values

**category:** Community & Outreach, Events & Training, Users & Identity, Content Management, Allocations, Resources, Operations, Metrics & Reporting

**track:** Support, Operations, Allocations, ACO

**access_level:** Public, Authenticated, Restricted, Internal Only, Sensitive, Varies

**priority:** High, Medium, Low

## Local Development

```bash
# Install dependencies (first time)
npm install

# Generate docs locally
python generate.py

# Validate without generating
python generate.py --validate

# Preview locally (then open http://localhost:8080)
cd docs && python -m http.server 8080

# Deploy to dbdocs manually
npm run dbdocs:build
```

## Project Structure

```
data-inventory/
├── data-sources/           # SOURCE OF TRUTH - edit these files
│   ├── announcements.md
│   ├── events.md
│   └── ...
├── docs/                   # Auto-generated (do not edit)
│   ├── index.md
│   ├── summary.md
│   ├── field-dictionary.md
│   ├── inventory.dbml
│   ├── inventory.json
│   └── heb-visualization.html
├── templates/              # HTML templates
│   └── heb-visualization.html
├── generate.py             # Generator script
├── schema.yaml             # Validation rules
└── package.json            # Node dependencies (dbdocs)
```

## Generated Outputs

| File | Description | Where to View |
|------|-------------|---------------|
| `index.md` | Landing page | GitHub Pages |
| `summary.md` | Stakeholder overview by track | GitHub Pages |
| `field-dictionary.md` | Detailed field documentation | GitHub Pages |
| `heb-visualization.html` | Interactive relationship diagram | GitHub Pages |
| `inventory.dbml` | Database schema | dbdocs.io |
| `inventory.json` | Machine-readable data | API/tools |

## Initial Setup (One-Time, Already Done)

These steps have already been completed for this repository. They're documented here for reference if setting up a new instance.

### GitHub Pages

1. Go to repo Settings → Pages
2. Source: Deploy from branch
3. Branch: `main`, folder: `/docs`

### dbdocs.io (CI Deployment)

1. Create account at https://dbdocs.io
2. Get API token from dbdocs dashboard
3. Add `DBDOCS_TOKEN` secret to GitHub repo (Settings → Secrets → Actions)

### dbdocs.io (Local Deployment - Optional)

Only needed if you want to manually deploy from your machine:

```bash
npm run dbdocs:login  # One-time authentication
npm run dbdocs:build  # Deploy
```
