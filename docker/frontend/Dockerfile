FROM node:lts-alpine

COPY /src/frontend /srv

WORKDIR /srv

RUN npm install

ENTRYPOINT npm run serve