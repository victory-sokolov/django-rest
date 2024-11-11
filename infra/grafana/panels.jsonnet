local g = import 'g.libsonnet';

{
  timeseries: {
    local timeSeries = g.panel.timeSeries,
    local fieldOverride = g.panel.timeSeries.fieldOverride,
    local custom = timeSeries.fieldConfig.defaults.custom,
    local options = timeSeries.options,

    base(title, targets):
      timeSeries.new(title)
      + timeSeries.queryOptions.withTargets(targets)
      + timeSeries.queryOptions.withDatasource('datasource', 'prometheus')
      + timeSeries.queryOptions.withInterval('1m')
      + timeSeries.standardOptions.withUnit('reqps')
      + timeSeries.gridPos.withW(24)
      + timeSeries.gridPos.withH(8)
      + options.legend.withDisplayMode('table')
      + options.legend.withCalcs([
        'lastNotNull',
        'max',
      ])
      + custom.withFillOpacity(10)
      + custom.withShowPoints('never'),

    short(title, targets):
      self.base(title, targets)
      + timeSeries.standardOptions.withUnit('short')
      + timeSeries.standardOptions.withDecimals(0),

    seconds(title, targets):
      self.base(title, targets)
      + timeSeries.standardOptions.withUnit('s')
      + custom.scaleDistribution.withType('log')
      + custom.scaleDistribution.withLog(10),

    // Haproxy
    haproxy_frontend: self.base,
    haproxy_backend: self.base,
    haproxy_avg_response_time: self.base,
    haproxy_status_codes: self.base,

    // Django Metrics


    heatmap: {
      local heatmap = g.panel.heatmap,
      local options = heatmap.options,

      base(title, targets):
        heatmap.new(title)
        + heatmap.queryOptions.withTargets(targets)
        + heatmap.queryOptions.withDatasource('datasource', 'prometheus')
        + heatmap.queryOptions.withInterval('1m')
        + options.withCalculate()
        + options.calculation.xBuckets.withMode('size')
        + options.calculation.xBuckets.withValue('1min')
        + options.withCellGap(2)
        + options.color.withMode('scheme')
        + options.color.withScheme('Spectral')
        + options.color.withSteps(128)
        + options.yAxis.withDecimals(0)
        + options.yAxis.withUnit('s'),
    },
  },
}
