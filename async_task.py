from celery import Celery 
from celery.signals import worker_ready
from blinker import signal
from kv_store import get_least_ttl, delete_key, REDIS_URL
import logging
import threading
import redis
from file_storage import delete_files

celery = Celery(
    broker=REDIS_URL
)
eviction_signal = signal("eviction-required")
FILES_TO_REMOVE = 1

@eviction_signal.connect
def trigger_eviction(sender, **extra):
    eviction.delay()

@celery.task
def eviction():
    entries = get_least_ttl()
    for key, ttl in entries[:FILES_TO_REMOVE]: # type: ignore
        print(f"deleting entry with key {key} and ttl {ttl} ")
        logging.info(msg=f"deleting entry with key {key} and ttl {ttl} ")
        delete_key(key=key)
        delete_files(code=key[5:])

@worker_ready.connect
def start_listener(sender, **kwargs):
    def listener():
        r = redis.from_url(REDIS_URL, decode_responses=True)
        pubsub = r.pubsub()
        pubsub.psubscribe('__keyevent@0__:expired')
        print("Waiting for file expiration signals...")
        for message in pubsub.listen():
            if message["type"] == "pmessage":
                expired_key = message["data"]
                code = expired_key[5:]
                logging.info(msg=f"Deleted files associated with code {code}")
                delete_files(code)
    
    thread = threading.Thread(target=listener, daemon=True)
    thread.start()
