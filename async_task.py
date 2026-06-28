from celery import Celery
from celery.signals import worker_ready
from kv_store import REDIS_URL, delete_key
import logging
import threading
import redis
from file_storage import delete_files
from logs import get_expired_uploads, mark_upload_cleaned

celery = Celery(broker=REDIS_URL)
celery.conf.update(
    timezone="UTC",
    beat_schedule={
        "reconcile-expired-uploads": {
            "task": "async_task.reconcile_expired_uploads",
            "schedule": 60.0,
        }
    },
)


def cleanup_code(code: str, source: str) -> bool:
    deleted = delete_files(code)
    if not deleted:
        logging.warning("Failed to delete S3 objects for code %s from %s", code, source)
        return False

    delete_key(f"code:{code}")
    mark_upload_cleaned(code)
    logging.info("Deleted files associated with code %s via %s", code, source)
    return True


@celery.task(name="async_task.reconcile_expired_uploads")
def reconcile_expired_uploads():
    entries = get_expired_uploads()
    for entry in entries:
        cleanup_code(str(entry["CODE"]), "periodic sweep")


@worker_ready.connect
def start_listener(sender, **kwargs):
    def listener():
        r = redis.from_url(REDIS_URL, decode_responses=True)
        pubsub = r.pubsub()
        pubsub.psubscribe("__keyevent@0__:expired")
        print("Waiting for file expiration signals...")
        for message in pubsub.listen():
            if message["type"] == "pmessage":
                expired_key = message["data"]
                if not str(expired_key).startswith("code:"):
                    continue
                code = expired_key[5:]
                cleanup_code(code, "redis expiry listener")

    thread = threading.Thread(target=listener, daemon=True)
    thread.start()
