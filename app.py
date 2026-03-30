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


# --- LOOP EM BACKGROUND (HUAWEI -> CLICKHOUSE) ---
def monitorar_huawei_background():
    click_house = ClickHouseDb()

    while True:
        try:
            _thread = threading.Thread(target=scrape_wan, args=(click_house, ax3_pro), daemon=True)
            _thread.start()

        except Exception as e:
            app.logger.error(f"Erro na coleta de background: {e}")

        time.sleep(5)

def scrape_wan(click_house: ClickHouseDb, ax3_pro: Ax3Pro):
    global DATA_VALID
    try:
        # 1. Faz a raspagem do roteador
        hosts = ax3_pro.scrape("/api/system/HostInfo")
        wan = ax3_pro.scrape("/api/ntwk/wan?type=active")

        lista_formatada = ax3_pro.get_metrics(hosts, wan, True)

        if lista_formatada:
            if isinstance(lista_formatada, str):
                lista_formatada = json.loads(lista_formatada)

            click_house.save_network_metrics(lista_formatada)

        DATA_VALID = True

    except Exception as e:
        app.logger.error(f"Erro na coleta de background: {e}")
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
    # Cria a thread separada pra não trancar o Flask
    thread_huawei = threading.Thread(target=monitorar_huawei_background, daemon=True)
    thread_huawei.start()

    # Roda o Flask pra servir as rotas e o healthcheck
    app.run(host='0.0.0.0', port=5000)