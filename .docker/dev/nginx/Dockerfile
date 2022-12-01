FROM nginx:latest
COPY .docker/dev/nginx/conf/default.conf /etc/nginx/conf.d/default.conf
RUN mkdir -p /etc/certs/
COPY .docker/dev/nginx/certs/*.pem /etc/certs/
COPY .docker/dev/nginx/options-ssl-nginx.conf /etc/nginx/
