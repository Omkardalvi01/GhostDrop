import redis
import logging

import os

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
FILE_TTL_SECONDS = int(os.environ.get("FILE_TTL_SECONDS", str(60 * 60 * 24)))
r = redis.from_url(REDIS_URL, decode_responses=True)
try:
    r.config_set("notify-keyspace-events", "Ex")
except Exception as e:
    logging.warning(f"Could not set notify-keyspace-events on Redis: {e}")

LIVE = 60 * 60 * 24
TEST = 60
THRESHOLD = 9999

with open("ttl_sort.lua", "r") as f:
    lua_script = f.read()
cached_script = r.register_script(lua_script)


def set_key(code: str, path: str, ttl_seconds: int = FILE_TTL_SECONDS) -> bool:
    try:
        r.set("code:" + code, path, ex=ttl_seconds)
    except Exception as e:
        logging.error(e)
        return False
    return True


def get_value(code):
    try:
        key = r.get("code:" + str(code))
        if not key:
            logging.error(msg="Key doesnt exist")
        return key
    except Exception as e:
        logging.error(e)
        return None


def get_all_keys():
    try:
        return [
            int(key.split(":", 1)[1])
            for key in r.scan_iter(match="code:*")
            if key.startswith("code:")
        ]
    except Exception as e:
        logging.error(e)
        return []


def get_size():
    try:
        return r.dbsize()
    except Exception as e:
        logging.error(e)
        return 0


def get_least_ttl():
    try:
        return cached_script(args=["code:*"])
    except Exception as e:
        logging.error(e)
        return []


def delete_key(key: str):
    try:
        r.delete(key)
    except Exception as e:
        logging.error(e)
