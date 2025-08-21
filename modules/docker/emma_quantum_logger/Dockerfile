FROM python:3.11-slim

WORKDIR /app
COPY ./emma_quantum_logger /app/

RUN pip install --no-cache-dir -r requirements.txt

VOLUME ["/secure/EmmaLogs"]

USER nobody

CMD ["python", "emma_remote_logger.py"]
