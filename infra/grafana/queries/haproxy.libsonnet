local g = import '../g.libsonnet';
local prometheusQuery = g.query.prometheus;

local variables = import '../variables.libsonnet';

{

  haproxy_requests:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            rate(
                haproxy_frontend_http_requests_total{job=~"$job", proxy="http-in", instance=~"$instance"}[$__rate_interval]
            )
        ) by (code) or vector(0)
      |||
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat('{{code}}'),

  haproxy_frontend_sessions:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            haproxy_frontend_current_sessions{job=~"$job", proxy="http-in", instance=~"$instance"}
        ) or vector(0)
      |||
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat('Total sessions by (frontend)'),

  haproxy_backend_sessions:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            haproxy_backend_current_sessions{job="haproxy-metrics", instance=~"$instance", proxy="server_backend"}
        ) or vector(0)
      |||
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat('Total sessions by (backend)'),

  haproxy_status_codes:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            rate(haproxy_frontend_http_responses_total{
                job="haproxy-metrics",
                proxy="http-in",
                instance=~"$instance"
            }[$__rate_interval])
        ) by (code)
      |||
    )
    + prometheusQuery.withLegendFormat(|||
      Frontend {{ code }}
    |||),

  haproxy_avg_response_time:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        avg(
         haproxy_backend_response_time_average_seconds{job=~"$job", proxy="server_backend", instance=~"$instance"}
        ) by (proxy)
      |||
    )
    + prometheusQuery.withLegendFormat(|||
      {{ proxy }} Response Time
    |||),

}
