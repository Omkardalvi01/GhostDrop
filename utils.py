import io
import random
from logging import raiseExceptions

from async_task import cleanup_code
from kv_store import get_all_keys, get_size, get_value
from thres_eviction import dequeue

# ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename) -> bool:
    parts = filename.split(".")
    if len(parts) != 2:
        return False
    return "." in filename


def valid_code(code) -> bool:
    if 0 > code or code >= 10000:
        return False
    if not get_value(code):
        return False
    return True


def make_code() -> int:

    size = get_size()

    if not isinstance(size, int):
        raise Exception("get_size() didnt return int")

    if size >= 9999:
        code = dequeue()
        if not cleanup_code(code=str(code), source="thres_eviction"):
            raise Exception("space exhausted")

        return code

    code = random.randint(1, 9999)
    exisiting_codes = get_all_keys()

    while code in exisiting_codes:
        code = random.randint(1, 9999)

    return code


class NamedBytes(io.BytesIO):
    def __init__(self, content, filename):
        super().__init__(content)
        self.filename = filename
