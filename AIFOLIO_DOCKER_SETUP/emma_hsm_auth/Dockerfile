FROM python:3.11-slim

WORKDIR /app
COPY ./emma_hsm_auth /app/

RUN pip install --no-cache-dir -r requirements.txt

USER nobody

CMD ["python", "emma_hsm_auth.py"]
