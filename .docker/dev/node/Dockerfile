FROM node:18-alpine

ARG UID=1000
ARG GID=1000

RUN deluser node
# RUN /usr/sbin/groupadd -g "${GID}" app  && /usr/sbin/useradd --create-home --no-log-init -u "${UID}" -g "${GID}" app
RUN addgroup -S -g "${GID}" app && adduser -S app -u "${UID}" -G app


# COPY . /app
RUN mkdir -p /app/ui
WORKDIR /app/ui
RUN npm install -g npm@9.1.2
# RUN npm install
EXPOSE 3000
USER app

CMD [ "npm", "start" ]