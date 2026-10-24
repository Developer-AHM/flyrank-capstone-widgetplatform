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