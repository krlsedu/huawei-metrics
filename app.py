import decimal
import json

from flask import Flask
from flask_cors import CORS

from services.Huawei import Ax3Pro

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ax3_pro = Ax3Pro()


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)


@app.route('/metrics')
def metrics():  # put application's code here
    scrape = ax3_pro.scrape("/api/system/HostInfo")
    return scrape, 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}


@app.route('/deviceinfo')
def deviceinfo():  # put application's code here
    scrape = ax3_pro.scrape("/api/system/deviceinfo")
    return scrape, 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
