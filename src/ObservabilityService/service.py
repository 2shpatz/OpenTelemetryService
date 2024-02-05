import os
import logging

from prometheus_client import start_http_server
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry import trace
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from prometheus_client import start_http_server, Gauge
import psutil
from flask import Flask, jsonify
import requests

class OpenTelemetry():
    def __init__(self) -> None:
        self.service_name = "observability"
        trace.set_tracer_provider(TracerProvider())
        self.tracer = trace.get_tracer(__name__)

        self.current_span = trace.get_current_span()

        # self.jaeger_exporter = JaegerSpanExporter(
        #                         service_name=self.service_name,
        #                         agent_host_name="localhost",
        #                         agent_port=6831,
        #                     )
        # 
        # self.span_processor = BatchSpanProcessor(self.jaeger_exporter)
        # trace.get_tracer_provider().add_span_processor(self.span_processor)

        
        # self.start_prometheus_client()

    def set_span(self):

        self.current_span.set_attribute("service.cpu", self.get_cpu())
        self.current_span.set_attribute("service.memory", self.get_memory())


    def do_work(self):
        with self.tracer.start_as_current_span("span-name") as span:
            # do some work that 'span' will track
            print("doing some work...")
            # When the 'with' block goes out of scope, 'span' is closed for you

    def start_prometheus_client(self):
        start_http_server(port=8000, addr="localhost")
        self.cpu_usage_metric = Gauge('cpu_usage_percent', 'CPU Usage Percentage')
        self.memory_usage_metric = Gauge('memory_usage_percent', 'Memory Usage Percentage')



class DataApi(OpenTelemetry):
    def __init__(self, port=os.getenv("APP_PORT")) -> None:
        super().__init__()
        self.app = Flask(__name__)
        self.app_port = port
        self.default_headers = {'accept': 'application/json'}
        opentelemetry.instrumentation.requests.RequestsInstrumentor().instrument()

        
    def get_request_headers(self):
        http_response = requests.get('https://httpbin.org/headers', headers=self.default_headers)
        json_resp = http_response.json()
        return jsonify(json_resp)
    
    def get_request_ip(self):
        http_response = requests.get('https://httpbin.org/ip', headers=self.default_headers)
        json_resp = http_response.json()
        return jsonify(json_resp)
    
    def get_request_user_agent(self):
        http_response = requests.get('https://httpbin.org/user-agent', headers=self.default_headers)
        json_resp = http_response.json()
        return jsonify(json_resp)
    

    def add_url_rules(self):
        # add API rules 
        self.app.add_url_rule('/headers', 'get_request_headers', self.get_request_headers)
        self.app.add_url_rule('/ip', 'get_request_ip', self.get_request_ip)
        self.app.add_url_rule('/user_agent', 'get_request_user_agent', self.get_request_user_agent)


    def run_app(self):
        # run the flask application for listening to HTTP requests
        logging.info("starting api server")
        self.add_url_rules()
        self.app.run(debug=True, port=self.app_port)

if __name__ == '__main__':
    service = DataApi()
    service.run_app()