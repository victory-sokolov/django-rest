ARG REDIS_VERSION=8.2.0@sha256:e7d6b261beaa22b1dc001f438b677f1c691ac7805607d8979bae65fe0615c2e6

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates
COPY redis.conf ./
COPY tls /redis/tls/

CMD [ "redis-server", "redis.conf" ]
