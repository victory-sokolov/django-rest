local g = import '../g.libsonnet';
local prometheusQuery = g.query.prometheus;
local variables = import '../variables.libsonnet';

{
  max_connections:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      'pg_settings_max_connections'
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat('PostgreSQL max_connections')
}
