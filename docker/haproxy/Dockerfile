FROM haproxy:3.2.0@sha256:b7c932c2d15208aa182dcebaea6d9605fdc2c72cdcd0badb8c89ab73f865a2fd

# Ensure the 'haproxy' user is already present
RUN id -u haproxy &>/dev/null || useradd -m haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
