ARG REDIS_VERSION=7.4.4@sha256:386e6c443372b9ba651d593baa881c802f3d3f093e2586602e05d6ba47ea733e

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates
COPY redis.conf ./
COPY tls /redis/tls/

CMD [ "redis-server", "redis.conf" ]
