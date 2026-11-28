import secrets

from app.repositories import widgets as repo
from app import config


def new_widget_id():
    return "w_" + secrets.token_hex(5)


def create_widget(owner_id, payload):
    return repo.create(new_widget_id(), owner_id, payload.model_dump())


def list_widgets(owner_id):
    return repo.list_for_owner(owner_id)


def get_widget(owner_id, widget_id):
    return repo.get_for_owner(widget_id, owner_id)


def replace_widget(owner_id, widget_id, payload):
    return repo.update_for_owner(widget_id, owner_id, payload.model_dump())


def delete_widget(owner_id, widget_id):
    return repo.delete_for_owner(widget_id, owner_id)

def get_public_config(widget_id):
    return repo.get_public(widget_id)


def build_snippet(widget_id):
    return f'<script src="{config.PUBLIC_BASE_URL}/widget.v1.js?id={widget_id}"></script>'