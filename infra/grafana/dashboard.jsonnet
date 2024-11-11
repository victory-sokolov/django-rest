local panels = import './panels.jsonnet';
local queries = import './queries.jsonnet';
local variables = import './variables.libsonnet';
local g = import 'g.libsonnet';

local var = g.dashboard.variable;
local row = g.panel.row;

g.dashboard.new('Django App Dashboard')
+ g.dashboard.withDescription('Djago App Metrics')
+ g.dashboard.withVariables([
  variables.datasource,
])
+ g.dashboard.withPanels(
  g.util.grid.makeGrid([
    row.new('Haproxy')
    + row.withPanels([
      panels.timeseries.haproxy_frontend(
        'Frontend Sessions',
        'Haproxy Frontend Sessions',
        queries.haproxy_frontend_sessions
      ),
      panels.timeseries.haproxy_backend(
        'Backend Sessions',
        'Haproxy Backend Sessions',
        queries.haproxy_backend_sessions
      ),
      panels.timeseries.haproxy_avg_response_time(
        'Average Response Time',
        'Haproxy FAverage Response Time',
        queries.haproxy_avg_response_time
      ),
      panels.timeseries.haproxy_avg_response_time(
        'Status Codes',
        'Haproxy Status Codes',
        queries.haproxy_status_codes
      ),
    ]),
  ], panelWidth=12)
)
