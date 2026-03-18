from kv_store import get_value
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