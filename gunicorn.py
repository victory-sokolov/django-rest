import ctypes
import os
from multiprocessing import Value
from djangoblog.metrics import SaturationMonitor

workers = 3
threads = 2
worker_class = "gevent"
timeout = 60
loglevel = "info"
proxy_protocol = True
forwarded_allow_ips = "*"
statsd_host = "localhost:9125"
statsd_prefix = "app"

# certfile = "certs/cert.crt"
# keyfile = "certs/cert.key"
# accesslog = "/path/to/gunicorn.access.log"
# errorlog = "/path/to/gunicorn.error.log"


METRIC_INTERVAL = os.environ.get("SATURATION_METRIC_INTERVAL", 5)

# Defaults to None, in which case no metrics will be sent.
statsd_host = os.environ.get("STATSD_HOST")


def when_ready(server):
    server.log.info("Starting SaturationMonitor")
    sm = SaturationMonitor(server)
    sm.start()
    server.log.debug(
        "busy workers = 0",
        extra={"metric": "gunicorn.busy_workers", "value": "0", "mtype": "gauge"},
    )
    server.log.debug(
        "total workers = 0",
        extra={
            "metric": "gunicorn.total_workers",
            "value": str(server.num_workers),
            "mtype": "gauge",
        },
    )


def pre_fork(server, worker):
    worker.busy = Value(ctypes.c_bool, False)


def pre_request(worker, req):
    worker.busy.value = True


def post_request(worker, req, environ, resp):
    worker.busy.value = False
