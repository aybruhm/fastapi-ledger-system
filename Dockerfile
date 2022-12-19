# pull from tiangolo image
FROM tiangolo/uvicorn-gunicorn:python3.9-slim

# set working directory
WORKDIR /ledger_be

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY requirements.txt .

# install dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r /ledger_be/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /ledger_be/

# run and make migrations
RUN chmod +x /ledger_be/run-migrations.sh
RUN ["./run-migrations.sh"]