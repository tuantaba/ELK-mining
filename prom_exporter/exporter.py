import os
import time
import json

from requests import NullHandler, exceptions

# from requests import exceptions
from prometheus_client import start_http_server, Gauge, Enum, multiprocess, Histogram
# import time
# import requests

#Function for compatibility with Gunicorn
def child_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)

JSONFILE = "output_epayment_duration_time.json"

class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """
    def __init__(self, polling_interval_seconds=5):
        self.polling_interval_seconds = polling_interval_seconds
        _INF = float("inf")
        
        self.duration_time = Histogram('duration_time', 'Duration Time in miliseconds', ['domain', 'method'], buckets=(50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000 , 4000, 6000, 8000, 10000, 20000, _INF))
        # self.loss_percent = Histogram('loss_percent', 'LOSS PERCENT in miliseconds', ['probe_hostname', 'dest_group'], buckets=(0, 1, 3, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, _INF))
     
        self.health = Enum("app_health", "Health", states=["healthy", "unhealthy"])

    def run_metrics_loop(self):
        """Metrics fetching loop"""
        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """
        try: 
            with open(JSONFILE, 'r') as file:
                all_data_load = json.load(file)
            #for json
            domain = "epayment.fpt.com.vn"
            for data_load in all_data_load:      
                try:
                    method = data_load["method"]
                except:
                    method = "unknow"

                
                try:
                    #latency default  la Seconds
                    duration_time = float(data_load["time_taken"])
                    print ("duration_time is ", duration_time)                
                    self.duration_time.labels(domain, method).observe(int(duration_time))                        
                except Exception as e:
                    print ("Error duration_time is:  ", e)

                # try:
                #     loss_percent = float(data_load["LOSS_PERCENT"])
                #     print ("loss_percent is ", loss_percent)                
                #     self.loss_percent.labels(probe_hostname, dest_group).observe(int(loss_percent))                        
                # except Exception as e:
                #     print ("Error loss_percent is:  ", e)

                # try:
                #     LOSS_PERCENT = data_load["LOSS_PERCENT"]
                #     self.LOSS_PERCENT.labels(probe_hostname, dest_group).set(LOSS_PERCENT)
                # except Exception as e:
                #     print ("Error LOSS_PERCENT is:  ", e)

        except:
            print ("Error: JSONFILE can not to read" )
                
def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "60s"))  #set to 60s  #86400
    exporter_port = int(os.getenv("EXPORTER_PORT", "9000"))

    app_metrics = AppMetrics(
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port, addr='127.0.0.1')
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()