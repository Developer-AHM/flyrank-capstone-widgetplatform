from psycopg.types.json import Jsonb

from app import db

COLUMNS = (
    "id, owner_id, type, title, description, fields, "
    "button_text, display_options, version, created_at, updated_at"
)


def create(widget_id, owner_id, data):
    with db.connect() as conn:
        return conn.execute(
            f"""INSERT INTO widgets
                (id, owner_id, type, title, description, fields, button_text, display_options)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING {COLUMNS}""",
            (
                widget_id,
                owner_id,
                data["type"],
                data["title"],
                data["description"],
                Jsonb(data["fields"]),
                data["button_text"],
                Jsonb(data["display_options"]),
            ),
        ).fetchone()


def list_for_owner(owner_id):
    with db.connect() as conn:
        return conn.execute(
            f"SELECT {COLUMNS} FROM widgets WHERE owner_id = %s ORDER BY created_at DESC",
            (owner_id,),
        ).fetchall()


def get_for_owner(widget_id, owner_id):
    with db.connect() as conn:
        return conn.execute(
            f"SELECT {COLUMNS} FROM widgets WHERE id = %s AND owner_id = %s",
            (widget_id, owner_id),
        ).fetchone()


def update_for_owner(widget_id, owner_id, data):
    with db.connect() as conn:
        return conn.execute(
            f"""UPDATE widgets
                SET type = %s, title = %s, description = %s, fields = %s,
                    button_text = %s, display_options = %s,
                    version = version + 1, updated_at = now()
                WHERE id = %s AND owner_id = %s
                RETURNING {COLUMNS}""",
            (
                data["type"],
                data["title"],
                data["description"],
                Jsonb(data["fields"]),
                data["button_text"],
                Jsonb(data["display_options"]),
                widget_id,
                owner_id,
            ),
        ).fetchone()


def delete_for_owner(widget_id, owner_id):
    with db.connect() as conn:
        cur = conn.execute(
            "DELETE FROM widgets WHERE id = %s AND owner_id = %s",
            (widget_id, owner_id),
        )
        return cur.rowcount > 0

PUBLIC_COLUMNS = "id, type, title, description, fields, button_text, display_options, version"


def get_public(widget_id):
    with db.connect() as conn:
        return conn.execute(
            f"SELECT {PUBLIC_COLUMNS} FROM widgets WHERE id = %s",
            (widget_id,),
        ).fetchone()