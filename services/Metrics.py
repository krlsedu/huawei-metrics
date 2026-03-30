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
        self.scrape_atual = 0  # Inicializa a rodada

    def to_metric(self, text):
        json_array = json.loads(text)

        # Grava a hora exata dessa rodada (em segundos)
        self.scrape_atual = time.time_ns() // 1000000000

        for json_item in json_array:
            host_ = json_item.get('ActualName', '')
            if host_ == "":
                host_ = json_item.get('HostName', '')

            id_ = json_item.get('ID', 'sem_id')
            ##replace - for _ and . for _
            id_ = id_.replace("-", "_").replace(".", "_")

            if host_ == "":
                host_ = f"Desconhecido_{id_}"

            tx = float(json_item.get('TxKBytes', 0))
            rx = float(json_item.get('RxKBytes', 0))

            self.add(id_, "tx", tx, host_)
            self.add(id_, "rx", rx, host_)

    def add(self, label, direction, value, host=None):
        # Puxa o carimbo da rodada atual
        ns = self.scrape_atual

        # --- DESVIO DA WAN ---
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

        # --- LÓGICA DA LAN ---
        sum_ = label + "_" + direction + '_sum'
        count_ = label + "_" + direction + '_count'
        rate_ = label + "_" + direction + '_rate'

        value_ = self.values.get(sum_)

        if value_ is None:
            # Primeira leitura do aparelho
            self.values[count_] = 0
            self.values[sum_] = value
            self.values[rate_] = 0.0

            self.timestamps[sum_] = ns
            self.timestamps[count_] = ns
            self.timestamps[rate_] = ns

            # AGORA SIM! Carimba o host e a direção nas três variáveis
            for l in [sum_, count_, rate_]:
                self.hosts[l] = host
                self.directions[l] = direction
        else:
            if value == value_:
                # O valor não mudou, a gente encerra a função AQUI
                # sem atualizar a data!
                return
            else:
                # O roteador atualizou os dados
                delta_time = ns - self.timestamps.get(sum_, ns)
                self.values[count_] = value - value_

                if delta_time > 0:
                    self.values[rate_] = (value - value_) / delta_time
                else:
                    self.values[rate_] = 0.0

                self.values[sum_] = value

                # Carimba a data nova pois teve tráfego
                self.timestamps[sum_] = ns
                self.timestamps[count_] = ns
                self.timestamps[rate_] = ns

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
        agora = datetime.datetime.now(datetime.timezone.utc)

        # Dicionário temporário pra agrupar as coisas
        agrupado = {}

        for label, value in self.values.items():
            # FILTRO MÁGICO: Só pega as métricas que foram carimbadas na rodada atual
            if self.timestamps.get(label) != getattr(self, 'scrape_atual', 0):
                continue

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
            if dados_dict: # Garante que não manda host vazio
                result.append({
                    "timestamp": agora,
                    "host": host,
                    # O json.dumps aqui é o que vai gerar a string que vai pra coluna "dados"
                    "dados": json.dumps(dados_dict)
                })

        return result