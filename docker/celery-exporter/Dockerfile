FROM danihodovic/celery-exporter:0.12.2

# Switch to root to install packages
USER root

# Install curl and msgpack
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    pip install --no-cache-dir msgpack && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the non-root user
USER nobody
