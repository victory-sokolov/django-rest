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
        )
      |||
    )
    + prometheusQuery.withIntervalFactor(2),

  haproxy_backend_sessions:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            increase(haproxy_backend_current_sessions{proxy="http-in"}[30s])
        )
      |||
    ),

}
