import redis 
from file_storage import delete_files
import logging 

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.psubscribe('__keyevent@0__:expired')

print("Waiting for file expiration signals...")

for message in pubsub.listen():
    if message["type"] == "pmessage":
        expired_key = message["data"]

        logging.info(msg=f"Deleted files associated with code {expired_key}")
        delete_files(expired_key)
