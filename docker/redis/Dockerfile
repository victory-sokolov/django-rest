ARG REDIS_VERSION=8.0.3@sha256:a1e0a3b3a6cedd74d8ba44805b2497b93851a296f08a44962fedc03f1c490b47

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates
COPY redis.conf ./
COPY tls /redis/tls/

CMD [ "redis-server", "redis.conf" ]
