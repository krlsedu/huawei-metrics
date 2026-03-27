import time
import datetime
import decimal
import json


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')


class PrometheusMetric:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.types = {}
        self.values = {}
        self.timestamps = {}
        self.hosts = {}
        self.directions = {}
        self.is_valid = True

    def to_metric(self, text):
        json_array = json.loads(text)
        for json_item in json_array:
            host_ = json_item['ActualName']
            if host_ == "":
                host_ = json_item['HostName']
            id_ = json_item['ID']
            ##replace - for _ and . for _
            id_ = id_.replace("-", "_").replace(".", "_")
            self.add(id_, "tx", float(json_item['TxKBytes']), host_)
            self.add(id_, "rx", float(json_item['RxKBytes']), host_)

    def add(self, label, direction, value, host=None):

        ns = time.time_ns() // 1000000000
        if host == "Wan":
            rate_label = label + "_" + direction + '_rate'
            sum_label = label + "_" + direction + '_sum'

            if rate_label in self.timestamps:
                delta_time = ns - self.timestamps[rate_label]
                trafego_estimado = value * delta_time
            else:
                trafego_estimado = 0

            self.values[rate_label] = value
            self.timestamps[rate_label] = ns
            self.hosts[rate_label] = host
            self.directions[rate_label] = direction

            self.values[sum_label] = self.values.get(sum_label, 0) + trafego_estimado
            self.timestamps[sum_label] = ns
            self.hosts[sum_label] = host
            self.directions[sum_label] = direction

            return

        sum_ = label + "_" + direction + '_sum'
        count_ = label + "_" + direction + '_count'
        try:
            value_ = self.values[sum_]
        except:
            value_ = None
        if value_ is None:
            self.values[count_] = 0
        else:
            self.values[count_] = value - value_
        self.values[sum_] = value
        self.timestamps[sum_] = ns
        self.timestamps[count_] = ns
        self.hosts[sum_] = host
        self.hosts[count_] = host
        self.directions[sum_] = direction
        self.directions[count_] = direction
        self.rate(label + "_" + direction + '_rate', direction, value, ns, host, value_)

    def rate(self, label, direction, value, timestamp, host=None, value_=None):
        if label not in self.values:
            self.values[label] = 0
            self.timestamps[label] = timestamp
            self.hosts[label] = host
            self.directions[label] = direction
        else:
            self.values[label] = (value - value_) / (timestamp - self.timestamps[label])
            self.timestamps[label] = timestamp

    # create metod to formar the output in prometheus format
    def format(self):
        result = []
        for label, value in self.values.items():
            host_ = self.hosts[label]
            direction_ = self.directions[label]
            if label.endswith("_rate"):
                result.append('#HELP ' + self.name + ' ' + self.description + ' - gauge')
                result.append(
                    f'huawei_{self.name}_rate{{host="{host_}", direction="{direction_}", unit="Kbps"}} {value * 8}')
            elif label.endswith("_count"):
                result.append('#HELP ' + self.name + ' ' + self.description + ' - counter')
                result.append(
                    f'huawei_{self.name}_count{{host="{host_}", direction="{direction_}",unit="KBytes"}} {value}')
            else:
                result.append('#HELP ' + self.name + ' ' + self.description + ' - sum')
                result.append(
                    f'huawei_{self.name}_sum{{host="{host_}", direction="{direction_}",unit="KBytes"}} {value}')
        result = '\n'.join(result)
        return result

    def format_as_json(self):
        # Pega a hora exata desse lote de métricas (mantendo o padrão UTC)
        agora = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # Dicionário temporário pra agrupar as coisas
        agrupado = {}

        for label, value in self.values.items():
            # Puxa o host e a direção (tx ou rx)
            host_ = self.hosts.get(label, "Desconhecido")
            direction_ = self.directions.get(label, "")

            # Se o host ainda não tá no nosso dicionário, cria uma casinha pra ele
            if host_ not in agrupado:
                agrupado[host_] = {}

            # Batiza a chave que vai ficar dentro do JSON e ajusta a matemática
            if label.endswith("_rate"):
                chave = f"{direction_}_rate_kbps"
                val = value * 8
            elif label.endswith("_count"):
                chave = f"{direction_}_count_kb"
                val = value
            else:
                chave = f"{direction_}_sum_kb"
                val = value

            # Joga o dado lá pra dentro do dicionário do host
            agrupado[host_][chave] = val

        # Agora transforma esse grupão num array de dicionários pro teu insert
        result = []
        for host, dados_dict in agrupado.items():
            result.append({
                "timestamp": agora,
                "host": host,
                # O json.dumps aqui é o que vai gerar a string que vai pra coluna "dados"
                "dados": json.dumps(dados_dict)
            })

        return result
