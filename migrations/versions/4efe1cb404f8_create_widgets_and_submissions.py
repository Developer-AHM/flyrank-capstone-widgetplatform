"""create widgets and submissions

Revision ID: 4efe1cb404f8
Revises: 
Create Date: 2026-10-24 12:17:19.354673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4efe1cb404f8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE widgets (
            id              TEXT PRIMARY KEY,
            owner_id        UUID NOT NULL,
            type            TEXT NOT NULL,
            title           TEXT NOT NULL,
            description     TEXT NOT NULL DEFAULT '',
            fields          JSONB NOT NULL DEFAULT '[]',
            button_text     TEXT NOT NULL DEFAULT 'Submit',
            display_options JSONB NOT NULL DEFAULT '{}',
            version         INTEGER NOT NULL DEFAULT 1,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE TABLE submissions (
            id              BIGSERIAL PRIMARY KEY,
            widget_id       TEXT NOT NULL REFERENCES widgets(id) ON DELETE CASCADE,
            owner_id        UUID NOT NULL,
            data            JSONB NOT NULL,
            ip              TEXT,
            country         TEXT,
            city            TEXT,
            geo_provider    TEXT,
            idempotency_key TEXT,
            created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("CREATE INDEX ix_widgets_owner ON widgets (owner_id)")
    op.execute("CREATE INDEX ix_submissions_widget_created ON submissions (widget_id, created_at DESC)")
    op.execute("CREATE INDEX ix_submissions_owner_created ON submissions (owner_id, created_at DESC)")
    op.execute("CREATE UNIQUE INDEX ux_submissions_idempotency ON submissions (widget_id, idempotency_key)")
    pass


def downgrade() -> None:
    op.execute("DROP TABLE submissions")
    op.execute("DROP TABLE widgets")
    pass
