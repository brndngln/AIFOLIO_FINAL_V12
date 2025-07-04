FROM python:3.11-slim

WORKDIR /app
COPY ./aifolio_worker /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "worker", "worker", "--loglevel=info"]
