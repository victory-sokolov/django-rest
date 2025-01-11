local g = import '../g.libsonnet';
local prometheusQuery = g.query.prometheus;

local variables = import '../variables.libsonnet';

{

  django_response_status:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            increase(
                django_http_responses_total_by_status_total{instance=~"$instance"}[$__rate_interval]
            )
        ) by (status) or vector(0)
      |||
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat(|||
      {{status}}
    |||),

  db_errors:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            max_over_time(
                django_db_errors_total{instance=~"$instance"}[$__rate_interval]
            )
        )
      |||
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat(|||
      Django ORM DB errors count
    |||),

  db_connection_errors:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            max_over_time(
                django_db_new_connection_errors_total{instance=~"$instance"}[$__rate_interval]
            )
        )
      |||
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat(|||
      Django ORM DB errors count
    |||),

  request_latency:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        histogram_quantile(
            0.50,
            sum(irate(
                django_http_requests_latency_seconds_by_view_method_bucket{
                    instance=~"$instance"
                }[$__rate_interval]
            )) by (le)
        ) or vector(0)
      |||
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat(|||
      Django Request latency
    |||),

  database_total_queries:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            irate(django_db_execute_total{instance=~"$instance"}[$__rate_interval])
        ) by (vendor) or vector(0)
      |||
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat(|||
      Database Total Queries
    |||),

  django_cache_hits:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            django_cache_get_hits_total{
                instance=~"$instance"
            }) by (backend) / sum(django_cache_get_total{
                instance=~"$instance"
            }) by (backend)
      |||
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat(|||
      Cache Hit Ratio
    |||),

  gunicorn_request_duration:
    prometheusQuery.new(
      '$' + variables.datasource.name,
      |||
        sum(
            app_gunicorn_request_duration or vector(0)
        )
      |||
    )
    + prometheusQuery.withIntervalFactor(2)
    + prometheusQuery.withLegendFormat('Average Request Duration'),

}
