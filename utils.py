ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename) -> bool:
    parts = filename.split(".")
    if len(parts) != 2 and parts[1].lower() in ALLOWED_EXTENSIONS:
        return False
    return "." in filename


def valid_code(code) -> bool:
    return True
