#!/bin/sh
set -e

redis-server /redis/redis.conf \
    --tls-port 6379 --port 0 \
    --tls-cert-file ./tls/redis.crt \
    --tls-key-file ./tls/redis.key \
    --tls-ca-cert-file ./tls/ca.crt
