local g = import '../g.libsonnet';
local prometheusQuery = g.query.prometheus;
local variables = import '../variables.libsonnet';

{
  client_active_connections:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      'sum(pgbouncer_pools_client_active_connections{database!="pgbouncer"}) by (database)'
    )
    + prometheusQuery.withLegendFormat('{{database}}'),

  server_active_connections:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      'sum(pgbouncer_pools_server_active_connections{database!="pgbouncer"}) by (database)'
    )
    + prometheusQuery.withLegendFormat('{{database}}'),

  client_waiting_connections:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      'sum(pgbouncer_pools_client_waiting_connections{database!="pgbouncer"}) by (database)'
    )
    + prometheusQuery.withLegendFormat('{{database}}'),

  server_idle_connections:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      'sum(pgbouncer_pools_server_idle_connections{database!="pgbouncer"}) by (database)'
    )
    + prometheusQuery.withLegendFormat('{{database}}'),
}
