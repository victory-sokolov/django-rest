local g = import './g.libsonnet';
local prometheusQuery = g.query.prometheus;

local variables = import './variables.libsonnet';

{
  haproxy_frontend_sessions:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            increase(haproxy_frontend_current_sessions{proxy="http-in"}[30s])
        ) or vector(0)
      |||
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat(|||
      Total sessions by (frontend)
    |||),

  haproxy_backend_sessions:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(haproxy_backend_current_sessions) or vector(0)
      |||
    )
    + prometheusQuery.withLegendFormat(|||
      Total sessions by (backend)
    |||),

  haproxy_status_codes:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            rate(haproxy_frontend_http_responses_total{proxy="http-in"}[30s])
        ) by (code) or vector(0)
      |||
    ),

  haproxy_avg_response_time:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        avg(
         haproxy_backend_response_time_average_seconds
        ) or vector(0)
      |||
    ),

}
