# pull from tiangolo image
FROM tiangolo/uvicorn-gunicorn:python3.9

# set working directory
WORKDIR /ledger_be

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /ledger_be/

# install dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r /ledger_be/requirements.dev.txt \
    && rm -rf /root/.cache/pip