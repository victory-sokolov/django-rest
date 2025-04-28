FROM haproxy:3.1.7@sha256:16415274ffb34bd08043c61ecdf4da6231b0843b020c06a0621c174630437afe

# Ensure the 'haproxy' user is already present
RUN id -u haproxy &>/dev/null || useradd -m haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
