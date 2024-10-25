FROM nginx:1.27

RUN apt-get update && apt-get install -y iputils-ping

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
