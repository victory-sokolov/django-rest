ARG REDIS_VERSION=7.4.0

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates and redis-entrypoint shell script
COPY redis-entrypoint.sh redis.conf ./
COPY tls /redis/tls/

RUN chmod +x ./redis-entrypoint.sh

CMD [ "./redis-entrypoint.sh" ]
