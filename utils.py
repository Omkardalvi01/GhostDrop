from kv_store import get_value, get_all_keys, get_size
import random 
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename) -> bool:
    parts = filename.split(".")
    if len(parts) != 2 and parts[1].lower() in ALLOWED_EXTENSIONS:
        return False
    return "." in filename


def valid_code(code) -> bool:
    if 0  > code or code >= 10000:
        return False
    if not get_value(code):
        return False
    return True 

def make_code() -> int:
    
    size = get_size()
    if size == 9999:
        raise Exception("MAX LIMIT reached")
        return -1
    
    code = random.randint(1, 9999)
    exisiting_codes = get_all_keys()
    
    while code in exisiting_codes:
        code = random.randint(1, 9999)
    
    return code 
    