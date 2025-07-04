# Emma HSM Auth Dockerfile
FROM python:3.10
RUN mkdir /app
COPY . /app
WORKDIR /app
CMD ["python", "emma_hsm_auth.py"]