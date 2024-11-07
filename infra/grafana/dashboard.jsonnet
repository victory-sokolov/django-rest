local g = import 'g.libsonnet';

local variables = import './variables.libsonnet';

local var = g.dashboard.variable;

g.dashboard.new('Django App Dashboard')
+ g.dashboard.withDescription('Djago App Metrics')
+ g.dashboard.withPanels([
  g.panel.timeSeries.new('Haproxy Frontend Sessions')
  + {
    description: 'This panel shows the Haproxy frontend sessions',
  }
  + g.panel.timeSeries.queryOptions.withTargets([
    g.query.prometheus.new(
      'Frontend Sessions',
      'sum(increase(haproxy_frontend_sessions_total{proxy="http-in"}[30s]))',
    ),
  ])
  + g.panel.timeSeries.queryOptions.withTargets([
    g.query.prometheus.new(
      'Frontend Sessions',
      'sum(increase(haproxy_frontend_sessions_total{proxy="http-in"}[30s]))',
    ),
  ])
  + g.panel.timeSeries.standardOptions.withUnit('reqps')
  + g.panel.timeSeries.gridPos.withW(24)
  + g.panel.timeSeries.gridPos.withH(8),
])
