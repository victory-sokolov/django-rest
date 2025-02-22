FROM haproxy:3.1.5@sha256:61ba467b5bf76a78c2331754451e53c41faad1348da7b757e172853e093d4879

# Ensure the 'haproxy' user is already present
RUN id -u haproxy &>/dev/null || useradd -m haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
