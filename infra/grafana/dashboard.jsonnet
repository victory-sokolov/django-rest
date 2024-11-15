local panels = import './panels.jsonnet';
local variables = import './variables.libsonnet';
local g = import 'g.libsonnet';

// Queries
local django = import './queries/django.libsonnet';
local haproxy = import './queries/haproxy.libsonnet';

local var = g.dashboard.variable;
local row = g.panel.row;

g.dashboard.new('Django App Dashboard')
+ g.dashboard.withDescription('Djago App Metrics')
+ g.dashboard.withVariables([
  variables.datasource,
  variables.rate,
  variables.instances,
])
+ g.dashboard.withPanels(
  g.util.grid.makeGrid(
    [
      row.new('Haproxy')
      + row.withPanels([
        panels.timeseries.haproxy_frontend(
          'Frontend Sessions',
          'Haproxy Frontend Sessions',
          haproxy.haproxy_frontend_sessions
        ),
        panels.timeseries.haproxy_backend(
          'Backend Sessions',
          'Haproxy Backend Sessions',
          haproxy.haproxy_backend_sessions
        ),
        panels.timeseries.haproxy_frontned_session_limit(
          'Frontend Session Limit',
          'Frontend Session Limit',
          haproxy.haproxy_frontned_session_limit
        ),
        panels.timeseries.haproxy_avg_response_time(
          'Average Response Time',
          'Haproxy FAverage Response Time',
          haproxy.haproxy_avg_response_time
        ),
        panels.timeseries.haproxy_avg_response_time(
          'Status Codes',
          'Haproxy Status Codes',
          haproxy.haproxy_status_codes
        ),
      ]),
      row.new('Django')
      + row.withPanels([
        panels.gauge.db_errors(
          'DB Query Errors',
          'Django DB Query Errors',
          django.db_errors
        ),
        panels.gauge.db_connection_errors(
          'DB Connection Errors',
          'Django Database Connection Errors',
          django.db_connection_errors
        ),
        panels.timeseries.request_latency(
          'Django Request Latency',
          'Django Request Latency',
          django.request_latency
        ),
        panels.timeseries.database_total_queries(
          'DB Total Queries',
          'Django Database Total Queries',
          django.database_total_queries
        ),
        panels.gauge.django_cache_hits(
          'Cache Hit Ratio',
          'Cache Hit Ratio',
          django.django_cache_hits
        ),
      ]),
    ], panelWidth=12
  ),
)
