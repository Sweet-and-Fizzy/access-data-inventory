---
id: affinity_groups
name: Affinity Groups
description: Community groups organized by interest or domain
category: Community & Outreach
track: Support
responsible_team: Support
access_level: Public
is_canonical: false
canonical_source: access-support-drupal
api_endpoint: https://support.access-ci.org/api/1.1/affinity_groups
dynamic: false
priority: High

mcp:
  available: true
  package: "@access-mcp/affinity-groups"
  tools:
    - name: search_affinity_groups
      method: GET
      description: Search and filter affinity groups
    - name: get_affinity_group_kb
      method: GET
      description: Get knowledge base resources for a group
    - name: get_affinity_group_events
      method: GET
      description: Get events associated with a group

fields:
  - name: nid
    type: int
    access: Public
    primary_key: true
    description: Node ID

  - name: uuid
    type: varchar
    access: Public
    mcp_name: id
    description: Unique identifier

  - name: title
    type: varchar
    access: Public
    required: true
    mcp_name: name
    description: Group name

  - name: body
    type: text
    access: Public
    mcp_name: description
    description: Group description (HTML cleaned in MCP)

  - name: group_id
    type: varchar
    access: Public
    required: true
    mcp_name: id
    description: URL-friendly group identifier

  - name: group_slug
    type: varchar
    access: Public
    description: URL slug for the group

  - name: category
    type: varchar
    access: Public
    mcp_name: category
    allowed_values: [ACCESS_RP, Community]
    description: Whether this is an RP-specific or community group

  - name: goals
    type: text
    access: Public
    description: Group goals and objectives

  - name: coordinator_id
    type: int
    access: Public
    references: users.user_id
    mcp_name: coordinator
    description: Group coordinator (exposed as name string in MCP)

  - name: slack_link
    type: varchar
    access: Public
    mcp_name: slack_link
    description: Link to Slack channel

  - name: mailing_list
    type: varchar
    access: Restricted
    description: Internal mailing list address

  - name: external_email_list
    type: varchar
    access: Restricted
    description: External email list address

  - name: github_org
    type: varchar
    access: Public
    description: GitHub organization URL

  - name: ask_ci_forum
    type: varchar
    access: Public
    mcp_name: ask_ci_forum
    description: Link to Ask.CI forum topic

  - name: meeting_notes_link
    type: varchar
    access: Public
    description: Link to meeting notes document

  - name: is_private
    type: boolean
    access: Restricted
    description: Whether the group is private

  - name: private_users
    type: text
    access: Restricted
    description: List of users with access to private group

  - name: image_id
    type: int
    access: Public
    description: Group logo/image

relationships:
  - type: has_one
    target: users
    field: coordinator_id
    description: Each group has a coordinator

  - type: has_many
    target: events
    through: affinity_group_events
    description: Groups host events

  - type: has_many
    target: announcements
    through: affinity_group_announcements
    description: Groups publish announcements

  - type: has_many
    target: users
    through: affinity_group_members
    description: Groups have members

  - type: has_many
    target: tags
    through: entity_tags
    description: Groups can be tagged
---

## Overview

Affinity groups are community-organized groups centered around shared interests, research domains, or resource provider communities. They provide a way for ACCESS users to connect with peers.

## Notes

- The MCP cleans HTML from the body field for cleaner display
- Coordinator is exposed as a name string in the MCP (not the user ID)
- Mailing list fields are restricted - not exposed via public API
- Private groups and their membership lists are restricted
