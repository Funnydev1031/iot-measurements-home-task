FROM node:lts

ARG FRONTEND_PORT

WORKDIR /app

COPY ./package.json /app/package.json

RUN npm install

COPY . /app

EXPOSE $FRONTEND_PORT

CMD ["sh", "/app/run.sh"]