---
id: announcements
name: Announcements
description: Resource provider and community announcements
category: Community & Outreach
track: Support
responsible_team: Support
access_level: Public
is_canonical: false
canonical_source: access-support-drupal
api_endpoint: https://support.access-ci.org/api/2.2/announcements
dynamic: false
priority: High

mcp:
  available: true
  package: "@access-mcp/announcements"
  tools:
    - name: search_announcements
      method: GET
      description: Search announcements with filters
    - name: get_my_announcements
      method: GET
      description: Get announcements authored by current user
    - name: create_announcement
      method: POST
      description: Create a new announcement
    - name: update_announcement
      method: PATCH
      description: Update an existing announcement
    - name: delete_announcement
      method: DELETE
      description: Delete an announcement

fields:
  - name: nid
    type: int
    access: Public
    primary_key: true
    description: Node ID

  - name: uuid
    type: varchar
    access: Public
    mcp_name: uuid
    description: Unique identifier

  - name: title
    type: varchar
    access: Public
    required: true
    mcp_name: title
    description: Announcement title

  - name: body
    type: text
    access: Public
    mcp_name: body
    description: HTML content

  - name: summary
    type: varchar
    access: Public
    mcp_name: summary
    description: Short summary text

  - name: published_date
    type: date
    access: Public
    mcp_name: published_date
    description: When the announcement was published

  - name: affiliation
    type: varchar
    access: Public
    mcp_name: affiliation
    allowed_values: [ACCESS Collaboration, Community]
    description: Whether this is an official ACCESS or community announcement

  - name: external_link
    type: varchar
    access: Public
    mcp_name: external_link
    description: Link to external resource

  - name: where_to_share
    type: text
    access: Internal Only
    mcp_name: where_to_share
    allowed_values: [Announcements page, Bi-Weekly Digest, Affinity Group page, Email to Affinity Group]
    description: Distribution channels for this announcement

  - name: affinity_group_id
    type: int
    access: Public
    mcp_name: affinity_group
    references: affinity_groups.nid
    description: Associated affinity group

  - name: image_id
    type: int
    access: Public
    description: Associated media image

relationships:
  - type: belongs_to
    target: affinity_groups
    field: affinity_group_id
    description: Announcements can be associated with an affinity group

  - type: has_many
    target: tags
    through: entity_tags
    description: Announcements can be tagged for categorization
---

## Overview

Announcements from resource providers and the ACCESS community. These are published on the ACCESS Support website and can be distributed via the bi-weekly digest email.

## Notes

- The announcements MCP supports full CRUD operations for authenticated users
- HTML content is preserved in the body field
- The `where_to_share` field is internal only - not exposed to public consumers
- Announcements can optionally be associated with an affinity group
