local variables = import './variables.libsonnet';
local g = import 'g.libsonnet';


{
  timeseries: {
    local timeSeries = g.panel.timeSeries,
    local fieldOverride = g.panel.timeSeries.fieldOverride,
    local custom = timeSeries.fieldConfig.defaults.custom,
    local options = timeSeries.options,

    base(title, description, targets):
      timeSeries.new(title)
      + timeSeries.queryOptions.withTargets(targets)
      + timeSeries.queryOptions.withDatasource(
        '$' + variables.datasource.type,
        '$' + variables.datasource.name
      )
      + timeSeries.queryOptions.withInterval('1m')
      + timeSeries.standardOptions.withUnit('reqps')
      + timeSeries.panelOptions.withDescription(description)
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

    // Haproxy
    haproxy_frontend: self.base,
    haproxy_backend: self.base,
    haproxy_avg_response_time: self.base,
    haproxy_status_codes: self.base,

    // Django
    request_latency: self.base,
    database_total_queries: self.base,

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

  gauge: {
    local _gauge = g.panel.gauge,
    local options = _gauge.options,

    gauge(title, description, targets):
      _gauge.new(title)
      + _gauge.queryOptions.withTargets(targets)
      + _gauge.queryOptions.withDatasource(
        '$' + variables.datasource.type,
        '$' + variables.datasource.name
      )
      + _gauge.queryOptions.withInterval('1m')
      + _gauge.panelOptions.withDescription(description)
      + _gauge.gridPos.withW(24)
      + _gauge.gridPos.withH(8),

    // Django Metrics
    db_errors: self.gauge,
    db_connection_errors: self.gauge,
    django_cache_hits: self.gauge,
  },

  stat: {
    local _stat = g.panel.stat,
    local options = _stat.options,

    gauge(title, description, targets):
      _stat.new(title)
      + _stat.queryOptions.withTargets(targets)
      + _stat.queryOptions.withDatasource(
        '$' + variables.datasource.type,
        '$' + variables.datasource.name
      )
      + _stat.queryOptions.withInterval('1m')
      + _stat.panelOptions.withDescription(description)
      + _stat.gridPos.withW(24)
      + _stat.gridPos.withH(8),

  },
}
