import redis
import logging
from typing import cast

import os

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(REDIS_URL, decode_responses=True)
r.config_set("notify-keyspace-events", "Ex")

LIVE = 60 * 60 * 24
TEST = 60
THRESHOLD = 1  # for test

with open("ttl_sort.lua", "r") as f:
    lua_script = f.read()
cached_script = r.register_script(lua_script)


def set_key(code: str, path: str) -> bool:
    try:
        r.set("code:" + code, path, ex=TEST)
    except Exception as e:
        logging.error(e)
        return False
    return True


def get_value(code):
    key = r.get("code:" + str(code))
    if not key:
        logging.error(msg="Key doesnt exist")
    return key


def get_all_keys():
    return [key for key in r.scan_iter()]


def get_size():
    from async_task import eviction_signal

    n = cast(int, r.dbsize())
    if n > THRESHOLD:
        eviction_signal.send()
    return n


def get_least_ttl():
    return cached_script(args=["code:*"])


def delete_key(key: str):
    print(f"deleting entry with key {key}")
    r.delete(key)

