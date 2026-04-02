import sqlite3
import logging

conn = sqlite3.Connection("log.db", check_same_thread=False)
conn.row_factory = sqlite3.Row

conn.execute("""CREATE TABLE IF NOT EXISTS LOGS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                UPLOADED_AT TEXT DEFAULT (datetime('now','localtime')), 
                IP_ADDR CHAR(12), 
                CODE INTEGER NOT NULL, 
                FILE_COUNT INTEGER NOT NULL,
                SIZE INTEGER NOT NULL); """)


def error_logging(func):
    def log(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RuntimeError as e:
            logging.error(f"Database error in {func.__name__}: {e}")

    return log


@error_logging
def add_to_logs(ip, code, files, size) -> None:
    conn.execute(
        """INSERT INTO LOGS(IP_ADDR, CODE, FILE_COUNT, SIZE) 
                    VALUES (?, ?, ?, ?)""",
        (ip, code, files, size),
    )
    conn.commit()


@error_logging
def get_metadata() -> tuple:
    curr = conn.execute(
        "select SUM(FILE_COUNT) as file_count, SUM(SIZE) as tranfer_size  from logs"
    )
    row = curr.fetchone()
    return row["file_count"], (row["tranfer_size"] or 0)
