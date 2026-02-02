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

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `nid` (PK) | int | Public |  | Drupal node ID |
| `uuid` | varchar | Public |  | Drupal UUID |
| `type` | varchar | Public |  | Drupal content type |
| `title` | varchar | Public |  | Content title |
| `body` | text | Public |  | Content body (HTML) |
| `status` | boolean | Internal Only |  | Published status |
| `created` | timestamp | Public |  | Content creation date |
| `changed` | timestamp | Public |  | Last modification date |
| `uid` | int | Restricted |  | Author user ID |

*PK = Primary Key, * = Required*

### Relationships

- **Has Many** `announcements`: Stores announcement content
- **Has Many** `events`: Stores event content (series and instances)
- **Has Many** `affinity_groups`: Stores affinity group content
- **Has Many** `tags`: Stores taxonomy terms
- **Has Many** `users`: Stores user accounts (Drupal users, linked to COManage)

<h2 id="affinity_groups">Affinity Groups</h2>

*Community groups organized by interest or domain*

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `nid` (PK) | int | Public |  | Node ID |
| `uuid` | varchar | Public | id | Unique identifier |
| `title` * | varchar | Public | name | Group name |
| `body` | text | Public | description | Group description (HTML cleaned in MCP) |
| `group_id` * | varchar | Public | id | URL-friendly group identifier |
| `group_slug` | varchar | Public |  | URL slug for the group |
| `category` | varchar | Public | category | Whether this is an RP-specific or community group |
| `goals` | text | Public |  | Group goals and objectives |
| `coordinator_id` | int | Public | coordinator | Group coordinator (exposed as name string in MCP) |
| `slack_link` | varchar | Public | slack_link | Link to Slack channel |
| `mailing_list` | varchar | Restricted |  | Internal mailing list address |
| `external_email_list` | varchar | Restricted |  | External email list address |
| `github_org` | varchar | Public |  | GitHub organization URL |
| `ask_ci_forum` | varchar | Public | ask_ci_forum | Link to Ask.CI forum topic |
| `meeting_notes_link` | varchar | Public |  | Link to meeting notes document |
| `is_private` | boolean | Restricted |  | Whether the group is private |
| `private_users` | text | Restricted |  | List of users with access to private group |
| `image_id` | int | Public |  | Group logo/image |

*PK = Primary Key, * = Required*

### Relationships

- **Has One** `users`: Each group has a coordinator
- **Has Many** `events`: Groups host events
- **Has Many** `announcements`: Groups publish announcements
- **Has Many** `users`: Groups have members
- **Has Many** `tags`: Groups can be tagged

<h2 id="announcements">Announcements</h2>

*Resource provider and community announcements*

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `nid` (PK) | int | Public |  | Node ID |
| `uuid` | varchar | Public | uuid | Unique identifier |
| `title` * | varchar | Public | title | Announcement title |
| `body` | text | Public | body | HTML content |
| `summary` | varchar | Public | summary | Short summary text |
| `published_date` | date | Public | published_date | When the announcement was published |
| `affiliation` | varchar | Public | affiliation | Whether this is an official ACCESS or community announcement |
| `external_link` | varchar | Public | external_link | Link to external resource |
| `where_to_share` | text | Internal Only | where_to_share | Distribution channels for this announcement |
| `affinity_group_id` | int | Public | affinity_group | Associated affinity group |
| `image_id` | int | Public |  | Associated media image |

*PK = Primary Key, * = Required*

### Relationships

- **Belongs To** `affinity_groups`: Announcements can be associated with an affinity group
- **Has Many** `tags`: Announcements can be tagged for categorization

<h2 id="comanage">COManage/ACCESS Identity</h2>

*User identity information*

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `user_id` (PK) | varchar | Sensitive |  | Internal user identifier |
| `access_id` | varchar | Sensitive |  | ACCESS username (e.g., jsmith) |
| `email` | varchar | Sensitive |  | User email address (PII) |
| `name` | varchar | Restricted |  | User's display name |
| `institution` | varchar | Restricted |  | User's institutional affiliation |

*PK = Primary Key, * = Required*

### Relationships

- **Has Many** `affinity_group_members`: Users can be members of affinity groups
- **Has Many** `event_registrations`: Users register for events

<h2 id="event_registrations">Event Registrations</h2>

*Registration and attendance data for events*

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `registration_id` (PK) | varchar | Restricted |  | Registration record ID |
| `event_id` | int | Restricted |  | Associated event |
| `user_id` | varchar | Restricted |  | Registered user |
| `registration_date` | timestamp | Restricted |  | When the registration was submitted |
| `attendance_status` | varchar | Restricted |  | Registration and attendance status |
| `referral_source` | varchar | Restricted |  | How the registrant heard about the event |
| `registrant_name` | varchar | Sensitive |  | Registrant's name (PII) |
| `registrant_email` | varchar | Sensitive |  | Registrant's email address (PII) |
| `registrant_institution` | varchar | Restricted |  | Registrant's institutional affiliation |
| `registrant_access_id` | varchar | Sensitive |  | Registrant's ACCESS ID (PII) |

*PK = Primary Key, * = Required*

### Relationships

- **Belongs To** `events`: Each registration is for a specific event
- **Belongs To** `users`: Each registration is linked to a user

<h2 id="events">Events and Training</h2>

*Workshops, webinars, training sessions, and office hours*

| Field | Type | Access | MCP Name | Description |
|-------|------|--------|----------|-------------|
| `id` (PK) | int | Public |  | Event ID |
| `uuid` | varchar | Public |  | Unique identifier |
| `title` * | varchar | Public | title | Event title |
| `description` | text | Public | description | Event description |
| `event_type` * | varchar | Public | type | Type of event |
| `skill_level` | varchar | Public | skill | Target skill level for attendees |
| `affiliation` | varchar | Public |  | Whether this is an official ACCESS or community event |
| `start_date` | timestamp | Public | start_date | Event start date and time |
| `end_date` | timestamp | Public | end_date | Event end date and time |
| `duration_hours` | decimal | Public | duration_hours | Calculated duration in hours (computed) |
| `starts_in_hours` | decimal | Public | starts_in_hours | Hours until event starts (negative if past) (computed) |
| `location` | varchar | Public |  | Physical location if applicable |
| `virtual_meeting_link` | varchar | Authenticated | virtual_meeting_link | Zoom/Teams link - requires authentication |
| `registration_url` | varchar | Public | registration_url | Link to register for the event |
| `contact` | varchar | Public | contact | Contact person or email |
| `speakers` | text | Public |  | Speaker names and affiliations |
| `tags` | text | Public | tags | Parsed from comma-separated tag list (computed) |
| `affinity_group_id` | int | Public |  | Associated affinity group |

*PK = Primary Key, * = Required*

### Relationships

- **Belongs To** `affinity_groups`: Events can be associated with an affinity group
- **Has Many** `tags`: Events are tagged for discovery
- **Has Many** `event_registrations`: Registration records for this event
