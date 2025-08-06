ARG REDIS_VERSION=8.2.0@sha256:b0efb06f6b4d8c1e2fd1b7c1e89e178d787b432b7b09286b4e7ea3dcdbac777a

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates
COPY redis.conf ./
COPY tls /redis/tls/

CMD [ "redis-server", "redis.conf" ]
