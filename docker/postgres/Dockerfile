ARG POSTGRES_VERSION=latest

FROM postgres:${POSTGRES_VERSION}

# Ensure the configuration directory exists
RUN mkdir -p /etc/postgresql/conf.d

# Copy your custom configuration file into the container
COPY ./custom-postgresql.conf /etc/postgresql/conf.d/custom-postgresql.conf

# Update the main postgresql.conf to include your custom settings
RUN echo "include_dir = '/etc/postgresql/conf.d'" >> /usr/share/postgresql/postgresql.conf.sample

# Start PostgreSQL with the custom configuration
CMD ["postgres", "-c", "config_file=/usr/share/postgresql/postgresql.conf.sample"]
