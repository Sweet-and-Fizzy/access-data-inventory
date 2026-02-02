---
id: event_registrations
name: Event Registrations
description: Registration and attendance data for events
category: Events & Training
track: Support
responsible_team: Support
access_level: Restricted
is_canonical: true
canonical_source: null
api_endpoint: null
dynamic: false
priority: Medium

mcp:
  available: false
  package: null
  tools: []
  notes: Contains PII; partial coverage via events MCP

fields:
  - name: registration_id
    type: varchar
    access: Restricted
    primary_key: true
    description: Registration record ID

  - name: event_id
    type: int
    access: Restricted
    references: events.id
    description: Associated event

  - name: user_id
    type: varchar
    access: Restricted
    references: users.user_id
    description: Registered user

  - name: registration_date
    type: timestamp
    access: Restricted
    description: When the registration was submitted

  - name: attendance_status
    type: varchar
    access: Restricted
    allowed_values: [registered, attended, no_show, cancelled]
    description: Registration and attendance status

  - name: referral_source
    type: varchar
    access: Restricted
    description: How the registrant heard about the event

  - name: registrant_name
    type: varchar
    access: Sensitive
    description: Registrant's name (PII)

  - name: registrant_email
    type: varchar
    access: Sensitive
    description: Registrant's email address (PII)

  - name: registrant_institution
    type: varchar
    access: Restricted
    description: Registrant's institutional affiliation

  - name: registrant_access_id
    type: varchar
    access: Sensitive
    description: Registrant's ACCESS ID (PII)

relationships:
  - type: belongs_to
    target: events
    field: event_id
    description: Each registration is for a specific event

  - type: belongs_to
    target: users
    field: user_id
    description: Each registration is linked to a user
---

## Overview

Event registration and attendance tracking data. This source contains records of who registered for events, whether they attended, and how they found out about the event.

## Notes

- Contains PII (names, emails, ACCESS IDs) - classified as Restricted/Sensitive
- Not exposed via MCP due to privacy concerns
- Partial event attendance counts may be available through the events MCP
- Useful for understanding training reach and effectiveness
- Referral source data helps track outreach effectiveness
