FROM haproxy:3.0.5

# Ensure the 'haproxy' user is already present
RUN id -u haproxy &>/dev/null || useradd -m haproxy

USER haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
