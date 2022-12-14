FROM python:3.10-alpine

ARG BACKEND_PORT

WORKDIR /app

RUN apk add --update gcc g++ build-base

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE $BACKEND_PORT

CMD ["sh", "/app/run.sh"]