import logging

from supabase import create_client

from app import config

log = logging.getLogger("uvicorn.error")

_client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)


def verify_token(token):
    try:
        response = _client.auth.get_user(token)
    except Exception as e:
        log.warning("token verification failed: %s: %s", type(e).__name__, e)
        return None
    if response is None or response.user is None:
        log.warning("token verification returned no user")
        return None
    return response.user