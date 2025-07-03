# Dockerfile for SAFE AI PMP Backend
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn pydantic
EXPOSE 8000
CMD ["uvicorn", "pmp_service:app", "--host", "0.0.0.0", "--port", "8000"]
