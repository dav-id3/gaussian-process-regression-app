FROM node:16.13-alpine3.14

WORKDIR /usr/src/app/openapi

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

RUN chmod 777 ./update.sh

CMD [ "./update.sh" ]