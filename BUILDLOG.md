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