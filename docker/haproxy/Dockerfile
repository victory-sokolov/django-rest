FROM haproxy:3.0.3

RUN useradd -m haproxy
USER haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
