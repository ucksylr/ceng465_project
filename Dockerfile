FROM python:3.9-alpine3.13
LABEL maintainer="ucksylr"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN adduser --disabled-password --no-create-home app && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    chmod -R +x /scripts

USER app

ENV PATH="/scripts:/py/bin:$PATH"


CMD [ "run.sh" ]