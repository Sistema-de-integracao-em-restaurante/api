# Stage 1: Base image
FROM python:3.9-slim as base
SHELL ["/bin/bash", "-c"]
WORKDIR /var/app/
RUN <<EOF
apt update
apt install build-essential libpq-dev -y
EOF
COPY src/ .

# Stage 2: Optmized deploy-ready image
FROM python:3.9-slim
WORKDIR /var/app/
COPY --from=base /var/app .
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:5000", "app:app"]
