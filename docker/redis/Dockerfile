ARG REDIS_VERSION=8.2.0@sha256:280d0c376e0c11fb173b0fd99e112ac33c5fdfbdbed3ff76e2618c1ee931a482

FROM redis:${REDIS_VERSION}

WORKDIR /redis

# Copy redis.conf config file, tls certificates
COPY redis.conf ./
COPY tls /redis/tls/

CMD [ "redis-server", "redis.conf" ]
