FROM haproxy:3.2.1

# Ensure the 'haproxy' user is already present
RUN id -u haproxy &>/dev/null || useradd -m haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
