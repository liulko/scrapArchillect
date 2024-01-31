import random

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS

import PrivateIPv4address

app = Flask(__name__)
CORS(app)
api = Api()

proxies = open('ips-datacenter_proxy1.txt', 'r').read().split('\n')


@app.route('/api/proxy', methods=['GET'])
def search_films():
    return proxies[random.randrange(0, len(proxies))]


if __name__ == "__main__":
    # app.run(host=PrivateIPv4address.host, port=5000, ssl_context=('/etc/letsencrypt/live/shkerebert.pp.ua/fullchain.pem', '/etc/letsencrypt/live/shkerebert.pp.ua/privkey.pem'))
    app.run(host=PrivateIPv4address.host, port=5000)
