ARG REDIS_VERSION=7.4.4@sha256:2582cc7e28849e4bdca8b991c3ede503ec706112d2eb2feb2191e9e980d37e92

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates
COPY redis.conf ./
COPY tls /redis/tls/

CMD [ "redis-server", "redis.conf" ]
