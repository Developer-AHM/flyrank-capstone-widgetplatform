from supabase import create_client

from app import config

_client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)


def verify_token(token):
    try:
        response = _client.auth.get_user(token)
    except Exception:
        return None
    if response is None or response.user is None:
        return None
    return response.user