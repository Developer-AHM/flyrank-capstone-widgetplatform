# BUILDLOG

AI assistant used: Claude. Entries are written per stage.

## Stage 0: Design

**Where AI helped**
- Drafted the data model, embed flow, API contracts, layer sketch and resilience rules in `docs/design.md`.
- Explained why choices were made (random widget ids, owner_id on submissions, 404 instead of 403 for other tenants' widgets, plain 201 for honeypot hits).

**What I decided or changed**
- Chose Python + FastAPI, Postgres in Docker, and Supabase for owner auth.
- Rejected the suggested non-goal of "no frontend dashboard". I will build one simple static HTML dashboard page, but only after all core requirements work. The non-goal became: no visual form builder, custom domains, or real CDN/hosting.
- Caught a typo in my local folder name (`platfrom`) and fixed it before the first commit.

**What I need to verify later**
- (write one thing you're unsure about, for example how CORS preflight works or why the geo fallback must be tested with mocks)# BUILDLOG

AI assistant used: Claude. Entries are written per stage.

## Stage 0: Design

**Where AI helped**
- Drafted the data model, embed flow, API contracts, layer sketch and resilience rules in `docs/design.md`.
- Explained why choices were made (random widget ids, owner_id on submissions, 404 instead of 403 for other tenants' widgets, plain 201 for honeypot hits).

**What I decided or changed**
- Chose Python + FastAPI, Postgres in Docker, and Supabase for owner auth.
- Rejected the suggested non-goal of "no frontend dashboard". I will build one simple static HTML dashboard page, but only after all core requirements work. The non-goal became: no visual form builder, custom domains, or real CDN/hosting.
- Caught a typo in my local folder name (`platfrom`) and fixed it before the first commit.

**What I need to verify later**
- (How CORS preflight works or why the geo fallback must be tested with mocks)

## Stage 1: Skeleton

**Where AI helped**
- Drafted the folder layout (routes/services/repositories), config loader, health route, Dockerfile and compose.yaml.
- Explained why the DB address differs between my machine (`localhost:5433`) and inside Docker (`db:5432`).

**What I changed / questioned**
- (one real thing, e.g. asked why the healthcheck replaces `restart: on-failure`)

**What I need to verify later**
- (How the API will connect to Postgres in Stage 2)

## Stage 2: Migrations

**Where AI helped**
- Drafted the Alembic setup, the `env.py` edit, and the migration SQL for `widgets`, `submissions` and four indexes.
- Explained why migrations beat `CREATE TABLE IF NOT EXISTS` (they can change an existing table later).

**What I changed / questioned**
- (one real thing, e.g. why `env.py` reads `.env` instead of `alembic.ini`)

**What I need to verify later**
- Whether the unique idempotency index behaves correctly with NULL keys (Stage 8).

## Stage 3: Auth and widget CRUD

**Where AI helped**
- Drafted the auth guard, widget schemas, repository, service, routes and the isolation script.

**What went wrong / what I learned**
- A stale server gave 404 on /me until it reloaded.
- Long commands pasted into the terminal got garbled and produced misleading 401s, so I moved the test into a script.
- owner_id must come only from the token; extra="forbid" rejects it in the body.

**To verify later**
- Why it gave 404 rather than 403 for another tenant's widget.

## Stage 4: Embed snippet and cached delivery

**Where AI helped**
- Drafted the snippet route, public config with ETag/304, versioned bundle and widget.v1.js.

**What went wrong / what I learned**
- Test script failed with `python: command not found` because the venv was not active in that tab.
- Pasting commands into a tab without `.env` loaded gave empty Supabase URL.
- Two checks failed intermittently (snippet 401, PUT not applied), then passed on three reruns. Added logging to verify_token to see the real cause if it recurs.
- Known limitation: a Supabase outage and a bad token both return 401; 503 would be more accurate.

**To verify later**
- Why the bundle is immutable and must never be edited after release.