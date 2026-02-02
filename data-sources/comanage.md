---
id: comanage
name: COManage/ACCESS Identity
description: User identity information
category: Users & Identity
track: Operations
responsible_team: Operations
access_level: Sensitive
is_canonical: true
canonical_source: null
api_endpoint: null
dynamic: false
priority: Low

mcp:
  available: false
  package: null
  tools: []
  notes: Identity data is sensitive and not suitable for AI/MCP exposure

fields:
  - name: user_id
    type: varchar
    access: Sensitive
    primary_key: true
    description: Internal user identifier

  - name: access_id
    type: varchar
    access: Sensitive
    description: ACCESS username (e.g., jsmith)

  - name: email
    type: varchar
    access: Sensitive
    description: User email address (PII)

  - name: name
    type: varchar
    access: Restricted
    description: User's display name

  - name: institution
    type: varchar
    access: Restricted
    description: User's institutional affiliation

relationships:
  - type: has_many
    target: affinity_group_members
    description: Users can be members of affinity groups

  - type: has_many
    target: event_registrations
    description: Users register for events
---

## Overview

COManage is the identity management system for ACCESS. It stores user identity information including ACCESS IDs, email addresses, and institutional affiliations.

## Notes

- This data source contains PII and is classified as Sensitive
- Not suitable for AI/MCP exposure
- Other teams will contribute to the full user data model
- Users may have multiple ACCESS IDs (legacy XSEDE + ACCESS)
- Institutional affiliations may be outdated

## Access Considerations

Identity data should only be accessed by:
- Named individuals with legitimate need
- Systems with explicit authorization
- Never exposed through public APIs or AI tools
