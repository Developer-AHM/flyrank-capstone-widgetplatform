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