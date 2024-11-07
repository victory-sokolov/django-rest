local g = import './g.libsonnet';
local var = g.dashboard.variable;

{
  datasource:
    var.datasource.new('datasource', 'Prometheus') +
    {
      label: 'Prometheus data source',
    },
}
