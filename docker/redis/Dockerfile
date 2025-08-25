ARG REDIS_VERSION=8.0.3@sha256:30abfcce7d0527dceb081dfa17cea0a6c2c315bf5a4ec7b2799118e852fdd553

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates
COPY redis.conf ./
COPY tls /redis/tls/

# skip permission changes
ENV SKIP_FIX_PERMS=1

CMD [ "redis-server", "redis.conf" ]
