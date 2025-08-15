FROM haproxy:3.2.4

# Ensure the 'haproxy' user is already present
RUN id -u haproxy &>/dev/null || useradd -m haproxy

# Use root to install packages
USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Switch back to haproxy runtime user
USER haproxy

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
