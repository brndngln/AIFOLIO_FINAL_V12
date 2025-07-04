FROM python:3.11-slim

WORKDIR /app
COPY ./aifolio_dashboard /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "emma_dashboard.py", "--server.port=8501"]
