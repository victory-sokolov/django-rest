local g = import './g.libsonnet';
local var = g.dashboard.variable;

{
  datasource:
    var.datasource.new('datasource', 'prometheus')
    + var.query.selectionOptions.withIncludeAll()
    + var.custom.generalOptions.withLabel('Data source'),

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
    var.query.new('instance')
    + var.query.withDatasourceFromVariable(self.datasource)
    + var.query.queryTypes.withLabelValues(
      'instance',
      '',
    )
    + var.query.selectionOptions.withIncludeAll()
    + var.query.selectionOptions.withMulti()
    + var.query.refresh.onTime()
    + var.query.generalOptions.withLabel('Instance')
    + { allValue: '.+' },


}
