FROM tiangolo/uvicorn-gunicorn:python3.9-slim

WORKDIR /ledger_be

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .