FROM haproxy:3.1.6@sha256:5faf31607d4333d02379f8642628edece8770fb428d90917f18bf3eec7bd2d84

# Ensure the 'haproxy' user is already present
RUN id -u haproxy &>/dev/null || useradd -m haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
