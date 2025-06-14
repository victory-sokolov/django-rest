FROM haproxy:3.2.1@sha256:9404d114ce0e7b124b696048619e264805c29439837b2e682c122843eed5ba64

# Ensure the 'haproxy' user is already present
RUN id -u haproxy &>/dev/null || useradd -m haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
