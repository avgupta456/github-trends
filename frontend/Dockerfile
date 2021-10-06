FROM node:16-alpine

WORKDIR /frontend

ENV PATH /frontend/node_modules/.bin:$PATH

COPY package.json yarn.lock /frontend/
RUN yarn install

COPY . /frontend

CMD ["yarn", "start"]