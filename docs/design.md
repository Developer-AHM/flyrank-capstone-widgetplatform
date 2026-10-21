# Design: Embeddable Widget & Lead-Capture Platform

## Decisions
- Lane: Python 3.12 + FastAPI
- Database: PostgreSQL (Docker), schema managed with migrations (Alembic)
- Owner auth: Supabase Auth (JWT verified on every owner request)
- Non-goal: no visual form builder, custom domains, or real CDN/hosting.
  Dashboard is one simple static HTML page, built last.

## Data model

### widgets
| Column | Type | Notes |
|---|---|---|
| id | text, primary key | random public id (e.g. `w_8f3k2x9a`), not sequential, so it can't be guessed or enumerated |
| owner_id | uuid, not null | Supabase user id: the tenant |
| type | text | `signup_form`, `contact_form`, `cta` |
| title | text | |
| description | text | |
| fields | jsonb | list of form fields (name, label, type, required) |
| button_text | text | |
| display_options | jsonb | |
| version | int | bumped on every edit, used for cache-busting config |
| created_at, updated_at | timestamptz | |

### submissions
| Column | Type | Notes |
|---|---|---|
| id | bigserial, primary key | |
| widget_id | text, FK to widgets | |
| owner_id | uuid, not null | copied from the widget, so tenant checks never need a join |
| data | jsonb | the validated form values |
| ip | text | visitor IP |
| country, city | text, nullable | null when geo enrichment fails |
| geo_provider | text, nullable | which provider answered (`a`, `b`, or null) |
| idempotency_key | text, nullable | retried submissions are stored once |
| created_at | timestamptz | |

### Indexes
- `widgets(owner_id)`: list my widgets
- `submissions(widget_id, created_at DESC)`: dashboard per widget, newest first
- `submissions(owner_id, created_at DESC)`: counts over time across all my widgets
- unique `submissions(widget_id, idempotency_key)`: idempotency guard

### Tenancy rule
`owner_id` comes from the verified Supabase token, never from the request body.
Every owner query includes `WHERE owner_id = <token user>`. A tenant asking for
someone else's widget gets 404, not 403, so existence isn't leaked.