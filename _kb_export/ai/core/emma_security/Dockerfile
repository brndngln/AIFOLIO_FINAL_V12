# Emma Quantum Logger Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY emma_remote_logger.py .
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential libffi-dev python3-dev && pip install --no-cache-dir -r requirements.txt
VOLUME ["/opt/emma_logs/"]
CMD ["python", "emma_remote_logger.py"]
