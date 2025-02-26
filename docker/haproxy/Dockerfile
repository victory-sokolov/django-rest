FROM haproxy:3.1.5@sha256:c3ca2f50e701297770a358ddcf62c432da11dc72e9a2054fed695cb6795d01eb

# Ensure the 'haproxy' user is already present
RUN id -u haproxy &>/dev/null || useradd -m haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
