## Requirement: Real persistence, schema as migrations, right indexes

Command: `alembic upgrade head`
Output: `Running upgrade -> 4efe1cb404f8, create widgets and submissions`

Command: `\di` in psql
Output: ix_widgets_owner, ix_submissions_widget_created, ix_submissions_owner_created, ux_submissions_idempotency present.

Command: `alembic downgrade base && alembic upgrade head`
Output: both ran cleanly (schema removed and rebuilt).