---
layout: default
title: Data Inventory
---

# Data Inventory

{: .intro}
Unified documentation for ACCESS data sources, APIs, and MCP tools.

## Goals

The ACCESS ecosystem spans dozens of data sources across multiple teams and tracks. This project exists to bring clarity and structure to that landscape so teams can work with data more effectively.

- **Catalog every ACCESS data source** in a single, version-controlled inventory
- **Document fields, relationships, and access levels** so consumers know what's available and how to use it
- **Enable discovery across tracks** by generating browsable docs and interactive diagrams
- **Power AI tools and automation** by providing machine-readable metadata that integrates with MCP servers, agents, and other workflows

## Data Sources

### Operations

| Source | Description | Access | |
|--------|-------------|--------|---|
| [COManage/ACCESS Identity](field-dictionary#comanage) | User identity information | Sensitive |  |

### Support

| Source | Description | Access | |
|--------|-------------|--------|---|
| [ACCESS Support Drupal](field-dictionary#access_support_drupal) | ACCESS Support website CMS - canonical storage for support content | Varies | [API](https://support.access-ci.org) |
| [Affinity Groups](field-dictionary#affinity_groups) | Community groups organized by interest or domain *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Public | [MCP](https://access-mcp.netlify.app/servers/affinity-groups) · [API](https://support.access-ci.org/api/1.1/affinity_groups) |
| [Announcements](field-dictionary#announcements) | Resource provider and community announcements *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Public | [MCP](https://access-mcp.netlify.app/servers/announcements) · [API](https://support.access-ci.org/api/2.2/announcements) |
| [Event Registrations](field-dictionary#event_registrations) | Registration and attendance data for events | Restricted |  |
| [Events and Training](field-dictionary#events) | Workshops, webinars, training sessions, and office hours *(sourced from [ACCESS Support Drupal](field-dictionary#access_support_drupal))* | Public | [MCP](https://access-mcp.netlify.app/servers/events) · [API](https://support.access-ci.org/api/2.2/events) |

## Resources

- [Fields](field-dictionary) — Field-level documentation
- [Connections](heb-visualization) — Interactive relationship visualization
- [Schema](erd) — Entity-relationship diagram
- [DBML](inventory.dbml) — Raw schema for dbdiagram.io
- [JSON](inventory.json) — Machine-readable export
- [Repository](https://github.com/Sweet-and-Fizzy/access-data-inventory) — Source files and contribution guide
