ARG REDIS_VERSION=8.0.2@sha256:1b835e5a8d5db58e8b718850bf43a68ef5a576fc68301fd08a789b20b4eecb61

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates
COPY redis.conf ./
COPY tls /redis/tls/

CMD [ "redis-server", "redis.conf" ]
