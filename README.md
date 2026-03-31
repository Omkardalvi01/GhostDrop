# GhostDrop

GhostDrop is a fast, temporary file sharing service that uses S3 for object storage and Redis for tracking file expiration (TTL). It supports securely uploading multiple files to a unique code that automatically self-destructs after a designated time.

## 🚀 Features
- **Ephemeral Storage:** Files automatically expire after a set time (TTL is handled via Redis Keyspace Notifications).
- **Multiple Files:** Supports selecting and uploading multiple files simultaneously in a single code payload.
- **Asynchronous Eviction:** File pruning and background event listening is handled efficiently via Celery workers and Redis.
- **Cloud Powered:** Uses AWS S3 for reliable blob storage.

## 🛠️ Architecture
- **Flask:** Serves the `/upload` and `/download` REST API endpoints.
- **Redis & Celery:** `kv_store.py` manages short-lived keys. `async_task.py` runs a background worker listening to Redis `__keyevent@0__:expired` channels to trigger S3 object deletion once the TTL has expired.
- **S3 (boto3):** Persists files with the code prefix and automatically deletes the prefix/folder when notified.

## 📦 Setup & Installation

### 1. Prerequisites
- Python 3.9+
- Redis Server (make sure keyspace events are enabled, the code does this via `r.config_set('notify-keyspace-events', 'Ex')`)
- AWS Account with S3 bucket

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
# The bucket is hardcoded to "ghostdrop" in file_storage.py
```

### 3. Running the Service

Start the Redis server locallly:
```bash
redis-server
```

Start the Celery background worker (this will also automatically spin up the Redis listener):
```bash
celery -A async_task worker --loglevel=info
```

Run the Flask application:
```bash
python app.py
```
The app will be accessible at `http://127.0.0.1:5000`.

## 📡 API Endpoints

### `POST /upload`
Upload one or multiple files. 
- **Form Data:** Use the key `file` (or `files`, `files[]`) to attach multiple files.
- **Response:**
  ```json
  {
      "status": "success",
      "message": "2 file(s) successfully uploaded",
      "code": 1234
  }
  ```

### `GET /download`
Download files associated with a specific code.
- **Query Params:** 
  - `code` (required): The 4-digit numeric code given upon upload.
  - `path` (optional): The local path to save the downloaded files (defaults to `~/Downloads`).
- **Response:**
  ```json
  {
      "status": "success"
  }
  ```

## 📝 Usage Example
Upload multiple files to GhostDrop:
```bash
curl -X POST -F "file=@memo.pdf" -F "file=@image.png" http://127.0.0.1:5000/upload
```
Download files:
```bash
curl "http://127.0.0.1:5000/download?code=1234"
```
