ARG REDIS_VERSION=8.0.3@sha256:f957ce918b51f3ac10414244bedd0043c47db44a819f98b9902af1bd9d0afcea

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates
COPY redis.conf ./
COPY tls /redis/tls/

# skip permission changes
ENV SKIP_FIX_PERMS=1

CMD [ "redis-server", "redis.conf" ]
