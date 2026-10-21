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

## Embed flow

1. The owner creates a widget through the authenticated API and receives a snippet:
   `<script src="http://localhost:8000/widget.v1.js?id=w_8f3k2x9a"></script>`
2. The customer pastes the snippet into any page (a different origin).
3. The browser loads `widget.v1.js`. It is a versioned bundle, so it is cached for a long time.
4. The script reads `id` from its own `src`, then calls `GET /widgets/{id}/config`. The config is cached briefly and carries an ETag.
5. The script renders a small form from the config (a div, the fields, a submit button, plus a hidden honeypot field).
6. On submit, the script sends `POST /submissions` cross-origin. The browser first sends an `OPTIONS` preflight, which the API must answer.
7. The API validates, rate-limits, spam-checks, enriches with geo, stores, then fires the email/webhook side effect. The owner sees the result in the dashboard.

## API contracts

### Path 1: Owner (authenticated, `Authorization: Bearer <Supabase JWT>`)
| Method | Path | Success | Errors |
|---|---|---|---|
| POST | `/widgets` | 201 + widget | 400/422 invalid, 401 no token |
| GET | `/widgets` | 200 list (own only) | 401 |
| GET | `/widgets/{id}/manage` | 200 | 401, 404 (also for other tenants) |
| PUT | `/widgets/{id}` | 200 (version bumped) | 401, 404, 422 |
| DELETE | `/widgets/{id}` | 204 | 401, 404 |
| GET | `/widgets/{id}/snippet` | 200 `{ "snippet": "<script ...>" }` | 401, 404 |
| GET | `/dashboard/submissions` | 200 paginated | 401 |
| GET | `/dashboard/stats` | 200 counts over time, per widget, geo breakdown | 401 |

### Path 2: Customer site (public, CORS, cached)
| Method | Path | Success | Cache |
|---|---|---|---|
| GET | `/widget.v1.js` | 200 JavaScript | `public, max-age=31536000, immutable` |
| GET | `/widgets/{id}/config` | 200 small JSON | `public, max-age=60` + ETag; 304 on match; 404 unknown |

### Path 3: Visitor (public, CORS, protected)
| Method | Path | Success | Errors |
|---|---|---|---|
| OPTIONS | `/submissions` | 204 with CORS headers | none |
| POST | `/submissions` | 201 `{ "id": ... }` (honeypot hit also returns a plain 201 to the bot, nothing stored) | 400/422 invalid, 404 unknown widget, 413 too large, 429 rate limited |

Request order inside `POST /submissions`: size check, validation, rate limit, honeypot, geo enrichment, store, side effect. Any failure after "store" must never change the response.

Error shape everywhere: `{ "error": "message" }`. No endpoint returns a 500 for bad input.

## Layers

```
routes/        HTTP only: parse request, call a service, return response
services/      logic: widget rules, spam check, geo chain, side effects, rate limit
repositories/  data only: SQL, one place that touches Postgres
```

Rules: routes never write SQL, repositories never raise HTTP errors, and services never see request objects. The geo providers and the email sender sit behind small interfaces in `services/`, so tests can swap in mocks.

## Resilience rules
- Geo: provider A, then B, then store without geo.
- Email/webhook: runs as a background job with retries and a failure log. A failure never changes the submission response.
- Idempotency: an `Idempotency-Key` header plus the unique `(widget_id, idempotency_key)` index means a retry is stored once.

## Non-goal
No visual form builder, custom domains, or real CDN/hosting. Everything runs locally.