FROM nginx:latest
COPY ./conf/default.conf /etc/nginx/conf.d/default.conf
RUN mkdir -p /etc/certs/
COPY ./certs/*.pem /etc/certs/
COPY ./options-ssl-nginx.conf /etc/nginx/
