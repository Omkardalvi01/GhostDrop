from celery import Celery 
from blinker import signal
from kv_store import get_least_ttl, delete_key
import logging
from file_storage import delete_files
celery = Celery(
    broker="redis://localhost:6379/0"
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


