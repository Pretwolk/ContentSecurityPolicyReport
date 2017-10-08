#!/usr/bin/env python3

import json, re, time, sys,yaml

from datetime import datetime,timezone
from elasticsearch import Elasticsearch
from flask import Flask
from flask import abort,redirect,url_for,request,jsonify

class ContentSecurityPolicyReport():

    config = {}

    def __init__(self):
        self.read_config()
        self.set_es()
        pass

    def read_config(self):
        with open('config/config.yaml') as file_config:
            self.config = yaml.load(file_config)

    def sanitize(self,in_str):
        regex = r'[^\w\d$]'
        if len(in_str) == 32:
            return re.sub(regex, repl='', string=in_str)
        else:
            self.json_response(403)

    def json_response(self,status = 200, msg=""):
        if status >= 400 and status < 499:
            abort(status,msg)
        elif status >= 500 and status < 599:
            abort(status,msg)
        elif status >= 200 and status < 299:
            return json.dumps({}), 200, {'Content-Type':'application/json'}

    def set_es(self):
        try:
            self.es = Elasticsearch([{'host': self.config['es']['host'],'port':self.config['es']['port']}])
        except:
            error = str(sys.exc_info())
            self.json_response(503)
    
    def put_es(self,index,doc_type, body):
        try:
            es = Elasticsearch([{'host': 'frsys04.pretwolk.nl','port':9200}])
            res = es.index(index=index, doc_type=doc_type, body=body)
        except:
            self.json_response(503)

    def validate_request(self, request):
        utcnow = datetime.now(timezone.utc)
        year = utcnow.year
        month = utcnow.month
        index = "report-csp-%s-%s-%s" % (self.client_id,year,month)

        if request.headers.get('Content-Type') != "application/csp-report":
            self.json_response(403)
        if not re.match(r'^Mozilla.*', request.headers.get('User-Agent')):
            self.json_response(403)
        if client_id not in self.config['client_ids']:
            self.json_response(403)

        csp_request = json.loads(str(request.data,'utf-8'), encoding='utf-8')
        csp_request['@timestamp'] = datetime.isoformat(utcnow)
        csp_request['client_id'] = self.client_id
        csp_request['user_agent'] = request.headers.get('User-Agent')
        csp_request['client_ip'] = request.headers.get('X-Forwarded-For')
        csp_request['content_length'] = request.headers.get('Content-Length')
        csp_request['http_version'] = request.environ.get('SERVER_PROTOCOL')

        return index, csp_request

    def process(self,client_id,request):
        self.client_id = self.sanitize(client_id)
        index, csp_request = self.validate_request(request)
        self.put_es(index,'text',csp_request)
        return 200

app = Flask(__name__)
@app.route("/api/v1/csp/<client_id>", methods=['POST'])
def apiv1csp(client_id):
    cspr.process(client_id,request)
    return cspr.json_response()

if __name__ == "__main__":
    cspr = ContentSecurityPolicyReport()
    app.run(host=cspr.config['network']['host'], port=cspr.config['network']['port'])

