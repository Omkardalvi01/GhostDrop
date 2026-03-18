import redis 
import logging
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.config_set('notify-keyspace-events', 'Ex')

LIVE = 60*60*24
TEST = 30

def set_key(code : str, path: str) -> bool:
    try: 
        r.set(code, path, ex= TEST)
    except Exception as e:
        logging.error(e)
        return False 
    return True 

def get_value(code):
    key = r.get(code)
    if not key:
        logging.error(msg="Key doesnt exist")
    return key