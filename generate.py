#!/usr/bin/env python3
"""
Generate various output formats from markdown+frontmatter data source files.

Outputs (in docs/ for GitHub Pages):
- docs/index.md - Landing page
- docs/summary.md - High-level stakeholder summary
- docs/field-dictionary.md - Detailed field reference
- docs/inventory.dbml - For dbdiagram.io
- docs/inventory.json - Machine-readable data

Note: docs/heb-visualization.md uses Jekyll layout (docs/_layouts/heb.html)

Usage:
    python generate.py
    python generate.py --validate  # Just validate, don't generate
"""

import sys
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime

# Directory setup
SCRIPT_DIR = Path(__file__).parent
DATA_SOURCES_DIR = SCRIPT_DIR / "data-sources"
DOCS_DIR = SCRIPT_DIR / "docs"
SCHEMA_FILE = SCRIPT_DIR / "schema.yaml"


def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    """Parse a markdown file with YAML frontmatter."""
    content = filepath.read_text()

    if not content.startswith('---'):
        raise ValueError(f"{filepath}: Missing YAML frontmatter")

    end_index = content.index('---', 3)
    frontmatter_str = content[3:end_index].strip()
    body = content[end_index + 3:].strip()

    frontmatter = yaml.safe_load(frontmatter_str)
    return frontmatter, body


def load_schema() -> dict:
    """Load the schema file."""
    if SCHEMA_FILE.exists():
        return yaml.safe_load(SCHEMA_FILE.read_text())
    return {}


def validate_source(source: dict, schema: dict) -> list[str]:
    """Validate a data source against the schema. Returns list of errors."""
    errors = []
    source_id = source.get('id', 'unknown')

    for field in schema.get('required_fields', []):
        if field not in source:
            errors.append(f"{source_id}: Missing required field '{field}'")

    allowed = schema.get('allowed_values', {})

    if 'category' in source and source['category'] not in allowed.get('category', []):
        errors.append(f"{source_id}: Invalid category '{source['category']}'")

    if 'track' in source and source['track'] not in allowed.get('track', []):
        errors.append(f"{source_id}: Invalid track '{source['track']}'")

    if 'access_level' in source and source['access_level'] not in allowed.get('access_level', []):
        errors.append(f"{source_id}: Invalid access_level '{source['access_level']}'")

    if 'priority' in source and source['priority'] not in allowed.get('priority', []):
        errors.append(f"{source_id}: Invalid priority '{source['priority']}'")

    for constraint in source.get('constraints', []):
        ctype = constraint.get('type', '')
        if ctype not in allowed.get('constraint_type', []):
            errors.append(f"{source_id}: Invalid constraint type '{ctype}'")

    for field in source.get('fields', []):
        field_name = field.get('name', 'unknown')

        if 'access' in field and field['access'] not in allowed.get('field_access', []):
            errors.append(f"{source_id}.{field_name}: Invalid access '{field['access']}'")

        if 'type' in field and field['type'] not in allowed.get('field_type', []):
            errors.append(f"{source_id}.{field_name}: Invalid type '{field['type']}'")

        if 'semantic_type' in field and field['semantic_type'] not in allowed.get('semantic_type', []):
            errors.append(f"{source_id}.{field_name}: Invalid semantic_type '{field['semantic_type']}'")

    return errors


def load_all_sources() -> list[dict]:
    """Load all data source files."""
    sources = []

    for filepath in sorted(DATA_SOURCES_DIR.glob("*.md")):
        try:
            frontmatter, body = parse_frontmatter(filepath)
            frontmatter['_body'] = body
            frontmatter['_filepath'] = str(filepath)
            sources.append(frontmatter)
        except Exception as e:
            print(f"Error loading {filepath}: {e}", file=sys.stderr)

    return sources




def generate_index(sources: list[dict]) -> str:
    """Generate the landing page following ACCESS brand guidelines."""
    mcp_count = sum(1 for s in sources if s.get('mcp', {}).get('available'))

    # Group sources by track
    by_track = {}
    for source in sources:
        track = source.get('track', 'Unknown')
        by_track.setdefault(track, []).append(source)

    lines = [
        "---",
        "layout: default",
        "title: Data Inventory",
        "---",
        "",
        "# Data Inventory",
        "",
        "{: .intro}",
        "Unified documentation for ACCESS data sources, APIs, and MCP tools.",
        "",
        "## Goals",
        "",
        "The ACCESS ecosystem spans dozens of data sources across multiple teams and tracks. This project exists to bring clarity and structure to that landscape so teams can work with data more effectively.",
        "",
        "- **Catalog every ACCESS data source** in a single, version-controlled inventory",
        "- **Document fields, relationships, and access levels** so consumers know what's available and how to use it",
        "- **Enable discovery across tracks** by generating browsable docs and interactive diagrams",
        "- **Power AI tools and automation** by providing machine-readable metadata that integrates with MCP servers, agents, and other workflows",
        "",
    ]

    # Data Sources by Track
    lines.append("## Data Sources")
    lines.append("")

    for track in sorted(by_track.keys()):
        track_sources = by_track[track]
        lines.append(f"### {track}")
        lines.append("")
        lines.append("| Source | Description | Access | |")
        lines.append("|--------|-------------|--------|---|")

        for source in sorted(track_sources, key=lambda x: x.get('name', '')):
            name = source.get('name', '')
            source_id = source.get('id', '')
            desc = source.get('description', '')
            access = source.get('access_level', '')
            mcp = source.get('mcp', {})

            # Links column
            links = []
            if mcp.get('available'):
                package = mcp.get('package', '')
                package_name = package.replace('@access-mcp/', '')
                links.append(f"[MCP](https://access-mcp.netlify.app/servers/{package_name})")
            if source.get('api_endpoint'):
                links.append(f"[API]({source.get('api_endpoint')})")
            links_str = " · ".join(links)

            # Add canonical source indicator
            canonical_note = ""
            if not source.get('is_canonical') and source.get('canonical_source'):
                canon_id = source['canonical_source'].replace('-', '_')
                canon_name = next((s.get('name', canon_id) for s in sources if s.get('id') == canon_id), canon_id)
                canonical_note = f" *(sourced from [{canon_name}](field-dictionary#{canon_id}))*"

            lines.append(f"| [{name}](field-dictionary#{source_id}) | {desc}{canonical_note} | {access} | {links_str} |")

        lines.append("")

    # Resources section
    lines.append("## Resources")
    lines.append("")
    lines.append("- [Fields](field-dictionary) — Field-level documentation")
    lines.append("- [Connections](heb-visualization) — Interactive relationship visualization")
    lines.append("- [Schema](erd) — Entity-relationship diagram")
    lines.append("- [DBML](inventory.dbml) — Raw schema for dbdiagram.io")
    lines.append("- [JSON](inventory.json) — Machine-readable export")
    lines.append("- [Repository](https://github.com/Sweet-and-Fizzy/access-data-inventory) — Source files and contribution guide")
    lines.append("")

    return "\n".join(lines)


def generate_field_dictionary(sources: list[dict]) -> str:
    """Generate a detailed field dictionary."""
    lines = [
        "---",
        "layout: default",
        "title: Fields",
        "---",
        "",
        "# Fields",
        "",
        "Field-level documentation for all ACCESS data sources.",
        "",
        "## Table of Contents",
        "",
    ]

    for source in sorted(sources, key=lambda x: x.get('name', '')):
        source_id = source.get('id', '')
        source_name = source.get('name', 'Unknown')
        lines.append(f"- [{source_name}](#{source_id})")

    lines.append("")

    for source in sorted(sources, key=lambda x: x.get('name', '')):
        source_id = source.get('id', '')
        lines.append(f"<h2 id=\"{source_id}\">{source.get('name', 'Unknown')}</h2>")
        lines.append("")
        lines.append(f"*{source.get('description', '')}*")
        lines.append("")

        # Add canonical source cross-link for non-authoritative sources
        if not source.get('is_canonical') and source.get('canonical_source'):
            canon_id = source['canonical_source'].replace('-', '_')
            canon_name = next((s.get('name', canon_id) for s in sources if s.get('id') == canon_id), canon_id)
            lines.append(f"> **Canonical source:** [{canon_name}](#{canon_id}) — this data is derived from the authoritative source above.")
            lines.append("")
        elif source.get('is_canonical') and source.get('provides_data_for'):
            derived = source['provides_data_for']
            derived_links = []
            for d in derived:
                d_name = next((s.get('name', d) for s in sources if s.get('id') == d), d)
                derived_links.append(f"[{d_name}](#{d})")
            lines.append(f"> **Authoritative source** for: {', '.join(derived_links)}")
            lines.append("")

        # Render use_cases
        use_cases = source.get('use_cases', [])
        if use_cases:
            lines.append("**Example questions this data can answer:**")
            lines.append("")
            for uc in use_cases:
                lines.append(f"- {uc}")
            lines.append("")

        # Render constraints
        constraints = source.get('constraints', [])
        if constraints:
            lines.append("**Constraints:**")
            lines.append("")
            for c in constraints:
                ctype = c.get('type', '').replace('_', ' ').title()
                lines.append(f"- **{ctype}:** {c.get('description', '')}")
            lines.append("")

        fields = source.get('fields', [])
        if not fields:
            lines.append("*No fields documented.*")
            lines.append("")
            continue

        lines.append("| Field | Type | Access | MCP Name | Description |")
        lines.append("|-------|------|--------|----------|-------------|")

        for field in fields:
            pk = " (PK)" if field.get('primary_key') else ""
            req = " *" if field.get('required') else ""
            computed = " (computed)" if field.get('computed') else ""
            mcp_name = field.get('mcp_name', '')
            sem = f" [{field['semantic_type']}]" if field.get('semantic_type') else ""

            lines.append(
                f"| `{field.get('name', '')}`{pk}{req} | "
                f"{field.get('type', '')} | "
                f"{field.get('access', '')} | "
                f"{mcp_name} | "
                f"{field.get('description', '')}{computed}{sem} |"
            )

        lines.append("")
        lines.append("*PK = Primary Key, * = Required, [type] = Semantic Type*")
        lines.append("")

        relationships = source.get('relationships', [])
        if relationships:
            lines.append("### Relationships")
            lines.append("")
            for rel in relationships:
                rel_type = rel.get('type', '').replace('_', ' ').title()
                target = rel.get('target', '')
                desc = rel.get('description', '')
                lines.append(f"- **{rel_type}** `{target}`: {desc}")
            lines.append("")

    return "\n".join(lines)


def generate_dbml(sources: list[dict]) -> str:
    """Generate DBML for dbdiagram.io."""
    lines = [
        "// ACCESS Data Inventory",
        f"// Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "// Source: data-sources/*.md",
        "",
        "// =============================================================================",
        "// DATA SOURCES",
        "// =============================================================================",
        "",
        "Enum data_source {",
    ]

    for source in sources:
        note_lines = [
            f"name: {source.get('name', '')}",
            f"description: {source.get('description', '')}",
            f"category: {source.get('category', '')}",
            f"track: {source.get('track', '')}",
            f"responsible_team: {source.get('responsible_team', '')}",
            f"access_level: {source.get('access_level', '')}",
            f"is_canonical: {str(source.get('is_canonical', False)).lower()}",
            f"canonical_source: {source.get('canonical_source') or 'null'}",
            f"mcp_available: {str(source.get('mcp', {}).get('available', False)).lower()}",
            f"mcp_package: {source.get('mcp', {}).get('package') or 'null'}",
            f"api_endpoint: {source.get('api_endpoint') or 'null'}",
            f"priority: {source.get('priority', '')}",
        ]

        lines.append(f"  {source.get('id', '')} [note: '''")
        for note_line in note_lines:
            lines.append(f"    {note_line}")
        lines.append("  ''']")
        lines.append("")

    lines.append("}")
    lines.append("")

    lines.append("// =============================================================================")
    lines.append("// ENTITIES")
    lines.append("// =============================================================================")
    lines.append("")

    for source in sources:
        fields = source.get('fields', [])
        if not fields:
            continue

        table_name = source.get('id', 'unknown')
        lines.append(f"Table {table_name} {{")

        for field in fields:
            field_line = f"  {field.get('name', '')} {field.get('type', 'varchar')}"

            attrs = []
            if field.get('primary_key'):
                attrs.append('pk')
            if field.get('required'):
                attrs.append('not null')

            note_parts = [f"access: {field.get('access', 'Public')}"]
            if field.get('mcp_name'):
                note_parts.append(f"mcp: {field.get('mcp_name')}")
            if field.get('computed'):
                note_parts.append("computed: true")
            if field.get('semantic_type'):
                note_parts.append(f"semantic: {field.get('semantic_type')}")
            if field.get('description'):
                # Escape apostrophes for DBML single-quoted strings
                desc = field.get('description').replace("'", "\\'")
                note_parts.append(desc)

            attrs.append(f"note: '{' | '.join(note_parts)}'")

            if attrs:
                field_line += f" [{', '.join(attrs)}]"

            lines.append(field_line)

        lines.append("")
        lines.append(f"  Note: '''")
        lines.append(f"    source: {source.get('id', '')}")
        lines.append(f"    description: {source.get('description', '')}")
        lines.append(f"    access_level: {source.get('access_level', '')}")

        use_cases = source.get('use_cases', [])
        if use_cases:
            lines.append(f"    use_cases:")
            for uc in use_cases:
                # Escape apostrophes for DBML
                uc_escaped = uc.replace("'", "\\'")
                lines.append(f"      - {uc_escaped}")

        constraints = source.get('constraints', [])
        if constraints:
            lines.append(f"    constraints:")
            for c in constraints:
                desc_escaped = c.get('description', '').replace("'", "\\'")
                lines.append(f"      - {c.get('type', '')}: {desc_escaped}")

        lines.append(f"  '''")
        lines.append("}")
        lines.append("")

    lines.append("// =============================================================================")
    lines.append("// RELATIONSHIPS")
    lines.append("// =============================================================================")
    lines.append("")

    # Build a map of table -> primary key field (only for tables we have)
    pk_map = {}
    table_ids = set()
    for source in sources:
        table_id = source.get('id', '')
        table_ids.add(table_id)
        for field in source.get('fields', []):
            if field.get('primary_key'):
                pk_map[table_id] = field.get('name')
                break

    for source in sources:
        for rel in source.get('relationships', []):
            if rel.get('type') == 'belongs_to' and rel.get('field'):
                source_table = source.get('id', '')
                target_table = rel.get('target', '')
                field = rel.get('field', '')

                # Only create ref if target table exists in our sources
                if target_table not in table_ids:
                    continue

                # Look up the target's primary key, default to 'id'
                target_pk = pk_map.get(target_table, 'id')
                lines.append(f"Ref: {source_table}.{field} > {target_table}.{target_pk}")

    lines.append("")

    return "\n".join(lines)


def generate_json(sources: list[dict]) -> str:
    """Generate JSON for visualization and tools."""
    clean_sources = []
    for source in sources:
        clean = {k: v for k, v in source.items() if not k.startswith('_')}
        clean_sources.append(clean)

    output = {
        "generated": datetime.now().isoformat(),
        "source_count": len(sources),
        "sources": clean_sources,
        "by_track": {},
        "by_category": {},
        "by_access_level": {},
    }

    for source in clean_sources:
        track = source.get('track', 'Unknown')
        output["by_track"].setdefault(track, []).append(source.get('id'))

        category = source.get('category', 'Unknown')
        output["by_category"].setdefault(category, []).append(source.get('id'))

        access = source.get('access_level', 'Unknown')
        output["by_access_level"].setdefault(access, []).append(source.get('id'))

    return json.dumps(output, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Generate outputs from data source files")
    parser.add_argument('--validate', action='store_true', help="Only validate, don't generate")
    args = parser.parse_args()

    schema = load_schema()
    sources = load_all_sources()

    if not sources:
        print("No data source files found in data-sources/", file=sys.stderr)
        sys.exit(1)

    print(f"Loaded {len(sources)} data source(s)")

    all_errors = []
    for source in sources:
        errors = validate_source(source, schema)
        all_errors.extend(errors)

    if all_errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in all_errors:
            print(f"  - {error}", file=sys.stderr)
        if args.validate:
            sys.exit(1)
        print("\nContinuing with generation despite errors...\n")
    else:
        print("Validation passed")

    if args.validate:
        return

    DOCS_DIR.mkdir(exist_ok=True)

    outputs = [
        ("index.md", generate_index(sources)),
        ("field-dictionary.md", generate_field_dictionary(sources)),
        ("inventory.dbml", generate_dbml(sources)),
        ("inventory.json", generate_json(sources)),
    ]

    for filename, content in outputs:
        filepath = DOCS_DIR / filename
        filepath.write_text(content)
        print(f"Generated: {filepath}")

    print("\nDone! Output is in docs/ - ready for GitHub Pages")


if __name__ == "__main__":
    main()
