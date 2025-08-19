ARG REDIS_VERSION=8.2.1@sha256:cc2dfb8f5151da2684b4a09bd04b567f92d07591d91980eb3eca21df07e12760

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates
COPY redis.conf ./
COPY tls /redis/tls/

# skip permission changes
ENV SKIP_FIX_PERMS=1

CMD [ "redis-server", "redis.conf" ]
