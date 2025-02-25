ARG POSTGRES_VERSION=17.4

FROM postgres:${POSTGRES_VERSION}

# Add the postgres user to the sudo group
RUN usermod -aG sudo postgres

# Ensure the configuration directory exists
RUN mkdir -p /etc/postgresql/conf.d

# Copy your custom configuration file into the container
COPY ./custom-postgresql.conf /etc/postgresql/conf.d/custom-postgresql.conf

RUN chmod 777 /etc/postgresql/conf.d/custom-postgresql.conf

# Script to initialise multiple databases
COPY create-multiple-postgresql-databases.sh /docker-entrypoint-initdb.d/

# Update the main postgresql.conf to include your custom settings
RUN echo "include_dir = '/etc/postgresql/conf.d'" >> /usr/share/postgresql/postgresql.conf.sample

ENTRYPOINT ["docker-entrypoint.sh"]

# Start PostgreSQL with the custom configuration
CMD ["postgres", "-c", "config_file=/usr/share/postgresql/postgresql.conf.sample"]
