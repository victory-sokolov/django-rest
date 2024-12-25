FROM prom/statsd-exporter:master

COPY ./statsd.yml /statsd/statsd.yml

CMD ["--statsd.mapping-config=/statsd/statsd.yml"]
