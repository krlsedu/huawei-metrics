import decimal
import json

from flask import Flask
from flask_cors import CORS

from services.Huawei import Ax3Pro
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ax3_pro = Ax3Pro()


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)


metrics = PrometheusMetrics(app, group_by='endpoint', default_labels={'application': 'HuaweiMetrics'})

is_valid = True

@app.route('/health')
def health():
    if is_valid:
        return "OK", 200
    else:
        return "NOK", 500


@app.route('/prometheus-metrics')
def metrics():  # put application's code here
    try:
        scrape = ax3_pro.scrape("/api/system/HostInfo")
        return scrape, 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}
    except Exception as e:
        is_valid = False
        return str(e), 500, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}


@app.route('/deviceinfo')
def deviceinfo():  # put application's code here
    scrape = ax3_pro.scrape("/api/system/deviceinfo")
    return scrape, 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
