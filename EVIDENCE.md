## Requirement: Real persistence, schema as migrations, right indexes

Command: `alembic upgrade head`
Output: `Running upgrade -> 4efe1cb404f8, create widgets and submissions`

Command: `\di` in psql
Output: ix_widgets_owner, ix_submissions_widget_created, ix_submissions_owner_created, ux_submissions_idempotency present.

Command: `alembic downgrade base && alembic upgrade head`
Output: both ran cleanly (schema removed and rebuilt).

## Requirement: Multi-tenant isolation (data layer)

Command: Python script creating a widget as owner A, then reading/listing/deleting as owner B.
Output:
A can get it: True
B can get it: False
A list size: 1 / B list size: 0
B can delete it: False
owner_id in body rejected: ValidationError

## Requirement: Multi-tenant isolation + authenticated widget CRUD

Command: `bash scripts/isolation_test.sh`
Output:
token lengths A/B: 944 947
1 no token (401): 401
2 owner reads (200): 200
3 other tenant reads (404): 404
4 B lists (200): 200   body: []
5 B updates A's (404): 404
6 B deletes A's (404): 404
7 smuggled owner_id (422): 422
8 A deletes own (204): 204