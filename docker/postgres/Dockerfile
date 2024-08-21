ARG POSTGRES_VERSION=latest

FROM postgres:${POSTGRES_VERSION}

COPY postgresql.conf /etc/postgresql

# Start PostgreSQL with the custom configuration
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
