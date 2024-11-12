local g = import './g.libsonnet';
local var = g.dashboard.variable;

{
  datasource:
    var.datasource.new('Prometheus', 'prometheus')
    + var.query.selectionOptions.withIncludeAll()
    + var.custom.generalOptions.withLabel('Prometheus data source'),

  rate:
    var.custom.new(
      'rate',
      values=['30s', '1m', '10m', '15m', '30m', '1h', '6h', '12h'],
    )
    + var.custom.generalOptions.withDescription(
      'Rate'
    )
    + var.custom.generalOptions.withLabel('Rate'),


  instances:
    var.custom.new(
      'instance',
      values=['haproxy:8405', 'app:80'],
    )
    + var.custom.generalOptions.withDescription(
      'Instances'
    )
    + var.query.withDatasourceFromVariable(self.datasource)
    + var.custom.generalOptions.withLabel('Instance')
    + var.custom.selectionOptions.withMulti(),

}
