FROM nginx:1.27

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get clean & apt-get update && apt-get install --no-install-recommends -y iputils-ping

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
