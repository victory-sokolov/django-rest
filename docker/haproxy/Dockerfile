FROM haproxy:3.2.3@sha256:9b0e65e0719cfbf9111df828e0da1a29cbf48917cf31081d5ae35f8453ca9fe0

# Ensure the 'haproxy' user is already present
RUN id -u haproxy &>/dev/null || useradd -m haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
