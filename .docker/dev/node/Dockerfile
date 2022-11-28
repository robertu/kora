FROM node:18-alpine

COPY . /app
WORKDIR /app/ui
RUN npm install -g npm@9.1.2
# RUN npm install
EXPOSE 3000
CMD [ "npm", "start" ]
