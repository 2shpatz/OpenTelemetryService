import os
import logging

from flask import Flask, jsonify
import requests

class DataApi():
    def __init__(self, port=os.getenv("APP_PORT")) -> None:
        super().__init__()
        self.app = Flask(__name__)
        self.app_port = port
        self.default_headers = {'accept': 'application/json'}
        
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