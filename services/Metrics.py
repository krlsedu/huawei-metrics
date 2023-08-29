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

    def to_metric(self, text):
        try:
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
        except Exception as e:
            print(e)
            print()
            pass

    def add(self, label, direction, value, host=None):

        ##get current time in seconds
        ns = time.time_ns() // 1000000000
        count_ = label + "_" + direction + '_count'
        try:
            value_ = self.values[count_]
        except:
            value_ = None
        self.values[count_] = value
        self.timestamps[count_] = ns
        self.hosts[count_] = host
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
                    f'{self.name}_rate{{host="{host_}", direction="{direction_}", unit="Kbps"}} {value * 8}')
            else:

                result.append('#HELP ' + self.name + ' ' + self.description + ' - counter')
                result.append(f'{self.name}_count{{host="{host_}", direction="{direction_}",unit="KBytes"}} {value}')
        result = '\n'.join(result)
        return result
