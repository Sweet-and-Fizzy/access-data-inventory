---
layout: default
title: Fields
---

# Fields

Field-level documentation for all ACCESS data sources.

## Table of Contents

- [ACCESS Support Drupal](#access_support_drupal)
- [Affinity Groups](#affinity_groups)
- [Announcements](#announcements)
- [COManage/ACCESS Identity](#comanage)
- [Event Registrations](#event_registrations)
- [Events and Training](#events)

<h2 id="access_support_drupal">ACCESS Support Drupal</h2>

*ACCESS Support website CMS - canonical storage for support content*

> **Authoritative source** for: [Announcements](#announcements), [Events and Training](#events), [Affinity Groups](#affinity_groups), [tags](#tags)

**Example questions this data can answer:**

- What content types are stored in the ACCESS Support CMS?
- When was a specific piece of content last modified?
- How many published nodes exist by content type?

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `nid` (PK) | int | Public |  | Drupal node ID [entity_id] |
| `uuid` | varchar | Public |  | Drupal UUID [uuid] |
| `type` | varchar | Public |  | Drupal content type [entity_type] |
| `title` | varchar | Public |  | Content title [entity_name] |
| `body` | text | Public |  | Content body (HTML) [entity_description] |
| `status` | boolean | Internal Only |  | Published status [entity_status] |
| `created` | timestamp | Public |  | Content creation date [date_created] |
| `changed` | timestamp | Public |  | Last modification date [date_modified] |
| `uid` | int | Restricted |  | Author user ID |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Has Many** `announcements`: Stores announcement content
- **Has Many** `events`: Stores event content (series and instances)
- **Has Many** `affinity_groups`: Stores affinity group content
- **Has Many** `tags`: Stores taxonomy terms
- **Has Many** `users`: Stores user accounts (Drupal users, linked to COManage)

<h2 id="affinity_groups">Affinity Groups</h2>

*Community groups organized by interest or domain*

> **Canonical source:** [ACCESS Support Drupal](#access_support_drupal) — this data is derived from the authoritative source above.

**Example questions this data can answer:**

- Which affinity groups are available for a specific research domain?
- Who coordinates a particular affinity group?
- What events are associated with an affinity group?
- How can I join or contact an affinity group?

**Constraints:**

- **Privacy:** Mailing lists, private group flags, and membership lists are restricted and must not be exposed through public APIs or AI tools.

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `nid` (PK) | int | Public |  | Node ID [entity_id] |
| `uuid` | varchar | Public | id | Unique identifier [uuid] |
| `title` * | varchar | Public | name | Group name [entity_name] |
| `body` | text | Public | description | Group description (HTML cleaned in MCP) [entity_description] |
| `group_id` * | varchar | Public | id | URL-friendly group identifier [entity_id] |
| `group_slug` | varchar | Public |  | URL slug for the group |
| `category` | varchar | Public | category | Whether this is an RP-specific or community group [entity_type] |
| `goals` | text | Public |  | Group goals and objectives [entity_summary] |
| `coordinator_id` | int | Public | coordinator | Group coordinator (exposed as name string in MCP) |
| `slack_link` | varchar | Public | slack_link | Link to Slack channel [url_external] |
| `mailing_list` | varchar | Restricted |  | Internal mailing list address [contact_info] |
| `external_email_list` | varchar | Restricted |  | External email list address [contact_info] |
| `github_org` | varchar | Public |  | GitHub organization URL [url_external] |
| `ask_ci_forum` | varchar | Public | ask_ci_forum | Link to Ask.CI forum topic [url_external] |
| `meeting_notes_link` | varchar | Public |  | Link to meeting notes document [url_external] |
| `is_private` | boolean | Restricted |  | Whether the group is private |
| `private_users` | text | Restricted |  | List of users with access to private group |
| `image_id` | int | Public |  | Group logo/image [media_ref] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Has One** `users`: Each group has a coordinator
- **Has Many** `events`: Groups host events
- **Has Many** `announcements`: Groups publish announcements
- **Has Many** `users`: Groups have members
- **Has Many** `tags`: Groups can be tagged

<h2 id="announcements">Announcements</h2>

*Resource provider and community announcements*

> **Canonical source:** [ACCESS Support Drupal](#access_support_drupal) — this data is derived from the authoritative source above.

**Example questions this data can answer:**

- What announcements have been published this week?
- Are there any announcements related to a specific affinity group?
- What resource provider updates have been shared recently?

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `nid` (PK) | int | Public |  | Node ID [entity_id] |
| `uuid` | varchar | Public | uuid | Unique identifier [uuid] |
| `title` * | varchar | Public | title | Announcement title [entity_name] |
| `body` | text | Public | body | HTML content [entity_description] |
| `summary` | varchar | Public | summary | Short summary text [entity_summary] |
| `published_date` | date | Public | published_date | When the announcement was published [date_published] |
| `affiliation` | varchar | Public | affiliation | Whether this is an official ACCESS or community announcement [affiliation] |
| `external_link` | varchar | Public | external_link | Link to external resource [url_external] |
| `where_to_share` | text | Internal Only | where_to_share | Distribution channels for this announcement |
| `affinity_group_id` | int | Public | affinity_group | Associated affinity group |
| `image_id` | int | Public |  | Associated media image [media_ref] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Belongs To** `affinity_groups`: Announcements can be associated with an affinity group
- **Has Many** `tags`: Announcements can be tagged for categorization

<h2 id="comanage">COManage/ACCESS Identity</h2>

*User identity information*

**Example questions this data can answer:**

- How many unique users are registered in ACCESS?
- Which institutions have the most ACCESS users?
- Is a specific user affiliated with a particular institution?

**Constraints:**

- **Privacy:** Contains PII (names, emails, ACCESS IDs). Must not be exposed through public APIs, AI tools, or MCP servers.
- **Acceptable Use:** Identity data may only be accessed by named individuals with legitimate need or systems with explicit authorization.
- **Regulatory:** Subject to institutional data handling agreements and FERPA considerations for student researchers.

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `user_id` (PK) | varchar | Sensitive |  | Internal user identifier [entity_id] |
| `access_id` | varchar | Sensitive |  | ACCESS username (e.g., jsmith) [entity_id] |
| `email` | varchar | Sensitive |  | User email address (PII) [person_email] |
| `name` | varchar | Restricted |  | User's display name [person_name] |
| `institution` | varchar | Restricted |  | User's institutional affiliation [institution] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Has Many** `affinity_group_members`: Users can be members of affinity groups
- **Has Many** `event_registrations`: Users register for events

<h2 id="event_registrations">Event Registrations</h2>

*Registration and attendance data for events*

**Example questions this data can answer:**

- How many people registered for a specific event?
- What is the attendance rate for training sessions?
- Which institutions are most represented at ACCESS events?
- How do registrants hear about ACCESS events?

**Constraints:**

- **Privacy:** Contains PII (names, emails, ACCESS IDs). Must not be exposed through public APIs or AI tools.
- **Acceptable Use:** Registration data may only be used for event management, reporting, and outreach effectiveness analysis. Individual-level data must not be shared outside authorized teams.

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `registration_id` (PK) | varchar | Restricted |  | Registration record ID [entity_id] |
| `event_id` | int | Restricted |  | Associated event |
| `user_id` | varchar | Restricted |  | Registered user |
| `registration_date` | timestamp | Restricted |  | When the registration was submitted [date_created] |
| `attendance_status` | varchar | Restricted |  | Registration and attendance status [entity_status] |
| `referral_source` | varchar | Restricted |  | How the registrant heard about the event |
| `registrant_name` | varchar | Sensitive |  | Registrant's name (PII) [person_name] |
| `registrant_email` | varchar | Sensitive |  | Registrant's email address (PII) [person_email] |
| `registrant_institution` | varchar | Restricted |  | Registrant's institutional affiliation [institution] |
| `registrant_access_id` | varchar | Sensitive |  | Registrant's ACCESS ID (PII) [entity_id] |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Belongs To** `events`: Each registration is for a specific event
- **Belongs To** `users`: Each registration is linked to a user

<h2 id="events">Events and Training</h2>

*Workshops, webinars, training sessions, and office hours*

> **Canonical source:** [ACCESS Support Drupal](#access_support_drupal) — this data is derived from the authoritative source above.

**Example questions this data can answer:**

- What training sessions are available for beginners this month?
- Which events are associated with a specific affinity group?
- How many office hours are scheduled for next week?
- What events require registration?

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `id` (PK) | int | Public |  | Event ID [entity_id] |
| `uuid` | varchar | Public |  | Unique identifier [uuid] |
| `title` * | varchar | Public | title | Event title [entity_name] |
| `description` | text | Public | description | Event description [entity_description] |
| `event_type` * | varchar | Public | type | Type of event [entity_type] |
| `skill_level` | varchar | Public | skill | Target skill level for attendees [skill_level] |
| `affiliation` | varchar | Public |  | Whether this is an official ACCESS or community event [affiliation] |
| `start_date` | timestamp | Public | start_date | Event start date and time [date_start] |
| `end_date` | timestamp | Public | end_date | Event end date and time [date_end] |
| `duration_hours` | decimal | Public | duration_hours | Calculated duration in hours (computed) [duration] |
| `starts_in_hours` | decimal | Public | starts_in_hours | Hours until event starts (negative if past) (computed) [time_relative] |
| `location` | varchar | Public |  | Physical location if applicable [location] |
| `virtual_meeting_link` | varchar | Authenticated | virtual_meeting_link | Zoom/Teams link - requires authentication [url_meeting] |
| `registration_url` | varchar | Public | registration_url | Link to register for the event [url_registration] |
| `contact` | varchar | Public | contact | Contact person or email [contact_info] |
| `speakers` | text | Public |  | Speaker names and affiliations [person_name] |
| `tags` | text | Public | tags | Parsed from comma-separated tag list (computed) [tags] |
| `affinity_group_id` | int | Public |  | Associated affinity group |

*PK = Primary Key, * = Required, [type] = Semantic Type*

### Relationships

- **Belongs To** `affinity_groups`: Events can be associated with an affinity group
- **Has Many** `tags`: Events are tagged for discovery
- **Has Many** `event_registrations`: Registration records for this event
