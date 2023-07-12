FROM python:3.11.4-slim-bullseye
LABEL mantainer="Francisco Oro"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt  /requirements.txt
COPY ./core /core
COPY ./scripts /scripts

WORKDIR /core 
EXPOSE 8000

RUN python3 -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get install -y build-essential libpq-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apt-get remove -y build-essential libpq-dev && \
    apt-get autoremove -y && \
    adduser --disabled-password --no-create-home apps && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R apps:apps /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"


USER apps

CMD [ "run.sh" ]