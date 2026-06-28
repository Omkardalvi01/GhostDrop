import logging
import os
import sqlite3
import threading
from datetime import datetime, timedelta, timezone

DB_PATH = os.getenv("LOG_DB_PATH", "log.db")
DEFAULT_TTL_SECONDS = int(os.getenv("FILE_TTL_SECONDS", str(60 * 60 * 24)))

conn = sqlite3.Connection(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row
DB_LOCK = threading.Lock()


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _expiry_from_ttl(ttl_seconds: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
    return expires_at.strftime("%Y-%m-%d %H:%M:%S")


def _ensure_schema() -> None:
    with DB_LOCK:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS LOGS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                UPLOADED_AT TEXT DEFAULT CURRENT_TIMESTAMP,
                EXPIRES_AT TEXT,
                CLEANED_AT TEXT,
                IP_ADDR CHAR(12),
                CODE INTEGER NOT NULL,
                FILE_COUNT INTEGER NOT NULL,
                SIZE INTEGER NOT NULL
            );"""
        )

        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(LOGS)").fetchall()
        }

        if "EXPIRES_AT" not in columns:
            conn.execute("ALTER TABLE LOGS ADD COLUMN EXPIRES_AT TEXT")
        if "CLEANED_AT" not in columns:
            conn.execute("ALTER TABLE LOGS ADD COLUMN CLEANED_AT TEXT")

        missing_expiry_rows = conn.execute(
            "SELECT ID, UPLOADED_AT FROM LOGS WHERE EXPIRES_AT IS NULL"
        ).fetchall()
        for row in missing_expiry_rows:
            uploaded_at = row["UPLOADED_AT"] or _utc_now()
            expires_at = datetime.strptime(
                uploaded_at, "%Y-%m-%d %H:%M:%S"
            ) + timedelta(seconds=DEFAULT_TTL_SECONDS)
            conn.execute(
                "UPDATE LOGS SET EXPIRES_AT = ? WHERE ID = ?",
                (expires_at.strftime("%Y-%m-%d %H:%M:%S"), row["ID"]),
            )

        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_logs_expiry ON LOGS(CLEANED_AT, EXPIRES_AT)"
        )
        conn.commit()


_ensure_schema()


def add_to_logs(ip, code, files, size, ttl_seconds: int = DEFAULT_TTL_SECONDS) -> bool:
    try:
        with DB_LOCK:
            conn.execute(
                """INSERT INTO LOGS(IP_ADDR, CODE, FILE_COUNT, SIZE, EXPIRES_AT)
                VALUES (?, ?, ?, ?, ?)""",
                (ip, code, files, size, _expiry_from_ttl(ttl_seconds)),
            )
            conn.commit()
        return True
    except Exception as e:
        logging.exception("Database error in add_to_logs: %s", e)
        return False


def get_expired_uploads(limit: int = 100):
    try:
        with DB_LOCK:
            rows = conn.execute(
                """SELECT CODE, EXPIRES_AT
                FROM LOGS
                WHERE CLEANED_AT IS NULL AND EXPIRES_AT IS NOT NULL AND EXPIRES_AT <= ?
                ORDER BY EXPIRES_AT ASC
                LIMIT ?""",
                (_utc_now(), limit),
            ).fetchall()
        return rows
    except Exception as e:
        logging.exception("Database error in get_expired_uploads: %s", e)
        return []


def mark_upload_cleaned(code) -> bool:
    try:
        with DB_LOCK:
            conn.execute(
                """UPDATE LOGS
                SET CLEANED_AT = ?
                WHERE CODE = ? AND CLEANED_AT IS NULL""",
                (_utc_now(), code),
            )
            conn.commit()
        return True
    except Exception as e:
        logging.exception("Database error in mark_upload_cleaned: %s", e)
        return False


def get_metadata() -> tuple:
    try:
        with DB_LOCK:
            curr = conn.execute(
                "SELECT SUM(FILE_COUNT) AS file_count, SUM(SIZE) AS tranfer_size FROM LOGS"
            )
            row = curr.fetchone()
        if not row:
            return 0, 0
        return row["file_count"] or 0, row["tranfer_size"] or 0
    except Exception as e:
        logging.exception("Database error in get_metadata: %s", e)
        return 0, 0
