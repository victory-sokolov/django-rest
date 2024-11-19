FROM prom/statsd-exporter:latest

COPY ./statsd.yml /statsd/statsd.yml

CMD ["--statsd.mapping-config=/statsd/statsd.yml"]
