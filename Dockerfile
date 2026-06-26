FROM python:3.11-slim-bookworm

# Prevent Python from writing pyc files to disc and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies directly
RUN pip install --no-cache-dir \
    "boto3>=1.42.69" \
    "celery>=5.6.2" \
    "flask>=3.1.3" \
    "flask-cors>=6.0.2" \
    "python-dotenv>=1.2.2" \
    "redis>=7.3.0" \
    gunicorn

# Copy project files
COPY app.py async_task.py file_storage.py kv_store.py logs.py utils.py ttl_sort.lua ./

# Create default log database file
RUN touch log.db

EXPOSE 5000

# Default command (can be overridden in docker-compose for celery)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
