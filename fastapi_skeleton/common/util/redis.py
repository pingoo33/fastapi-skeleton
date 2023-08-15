from fastapi_skeleton.config.env import config
from fastapi_skeleton.config.redis import redis

REFRESH_TOKEN_EXPIRE_MINUTES = config.get("security.jwt.expire.refresh")


def save_refresh_key(refresh_key: str, user_id: int):
    with redis.get_connection() as conn:
        conn.set(refresh_key, user_id, ex=REFRESH_TOKEN_EXPIRE_MINUTES * 60)


def delete_refresh_key(refresh_key: str):
    with redis.get_connection() as conn:
        if conn.get(refresh_key) is not None:
            conn.delete(refresh_key)


def find_user_id_by_refresh_key(refresh_key: str):
    with redis.get_connection() as conn:
        return int(conn.get(refresh_key))
