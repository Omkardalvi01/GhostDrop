import redis 
import logging
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def set_key(code : str, path: str) -> bool:
    try: 
        r.set(code, path, ex= 60*60*24)
    except Exception as e:
        logging.error(e)
        return False 
    return True 

def get_value(code):
    key = r.get(code)
    if not key:
        logging.log(msg="Key doesnt exist", level=1)
    return key