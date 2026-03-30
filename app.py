import os
import time
import threading
import decimal
import json

from flask import Flask
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

from service.ClickHouseDb import ClickHouseDb
from services.Huawei import Ax3Pro

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ax3_pro = Ax3Pro()


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)


metrics = PrometheusMetrics(app, group_by='endpoint', default_labels={'application': 'HuaweiMetrics'})

DATA_VALID = True


# --- BACKGROUND LOOP (HUAWEI -> CLICKHOUSE) ---
def monitor_huawei_background(time_sleep: int = 5):
    click_house = ClickHouseDb()

    while True:
        try:
            _thread = threading.Thread(target=scrape_wan, args=(click_house, ax3_pro), daemon=True)
            _thread.start()

        except Exception as e:
            app.logger.error(f"Background collection error: {e}")
        
        time.sleep(time_sleep)

def scrape_wan(click_house: ClickHouseDb, ax3_pro: Ax3Pro):
    global DATA_VALID
    try:
        # 1. Scrapes the router
        hosts = ax3_pro.scrape("/api/system/HostInfo")
        wan = ax3_pro.scrape("/api/ntwk/wan?type=active")

        formatted_list = ax3_pro.get_metrics(hosts, wan, True)

        if formatted_list:
            if isinstance(formatted_list, str):
                formatted_list = json.loads(formatted_list)

            click_house.save_network_metrics(formatted_list)

        DATA_VALID = True

    except Exception as e:
        app.logger.error(f"Background collection error: {e}")
        DATA_VALID = False

@app.route('/health')
def health():
    if DATA_VALID:
        return "OK", 200
    else:
        return "NOK", 500


@app.route('/prometheus-metrics')
def get_prometheus_metrics():
    try:
        hosts = ax3_pro.scrape("/api/system/HostInfo")
        wan = ax3_pro.scrape("/api/ntwk/wan?type=active")
        scrape = ax3_pro.get_metrics(hosts, wan)
        return scrape, 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}
    except Exception as e:
        global DATA_VALID
        DATA_VALID = False
        return str(e), 500, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}


@app.route('/json-metrics')
def metrics_json():
    try:
        hosts = ax3_pro.scrape("/api/system/HostInfo")
        wan = ax3_pro.scrape("/api/ntwk/wan?type=active")
        scrape = ax3_pro.get_metrics(hosts, wan, True)
        return scrape, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        global DATA_VALID
        DATA_VALID = False
        return str(e), 500, {'Content-Type': 'application/json'}


@app.route('/deviceinfo')
def deviceinfo():
    try:
        scrape = ax3_pro.scrape("/api/system/deviceinfo")
        return scrape, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        global DATA_VALID
        DATA_VALID = False
        return str(e), 500, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    # Create separate thread to not block Flask
    time_sleep = os.getenv('TIME_SLEEP', 5)
    time_sleep = int(time_sleep)
    if time_sleep > 0:
        thread_huawei = threading.Thread(target=monitor_huawei_background, args=(time_sleep,), daemon=True)
        thread_huawei.start()

    # Run Flask to serve routes and healthcheck
    app.run(host='0.0.0.0', port=5000)