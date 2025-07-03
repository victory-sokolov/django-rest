FROM haproxy:3.2.2@sha256:38659af7e27e075cfd6b5a66b5694f42640eac263d13522b27327d88f9566525

# Ensure the 'haproxy' user is already present
RUN id -u haproxy &>/dev/null || useradd -m haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
