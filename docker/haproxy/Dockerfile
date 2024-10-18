FROM haproxy:3.0.5

RUN useradd -m haproxy || true
USER haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
