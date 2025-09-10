ARG REDIS_VERSION=8.2.1@sha256:acb90ced0bd769b7c04cb4c32c4494ba7b3e0ee068bdbfff0eeb0d31c2a21078

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates
COPY redis.conf ./
COPY tls /redis/tls/

# skip permission changes
ENV SKIP_FIX_PERMS=1

CMD [ "redis-server", "redis.conf" ]
