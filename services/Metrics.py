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
        self.current_scrape = 0  # Initializes the current scraping round

    def to_metric(self, text):
        json_array = json.loads(text)

        # Records the exact time of this scrape (in seconds)
        self.current_scrape = time.time_ns() // 1000000000

        for json_item in json_array:
            host_ = json_item.get('ActualName', '')
            if host_ == "":
                host_ = json_item.get('HostName', '')

            id_ = json_item.get('ID', 'no_id')
            # replace - for _ and . for _
            id_ = id_.replace("-", "_").replace(".", "_")

            if host_ == "":
                host_ = f"Unknown_{id_}"

            tx = float(json_item.get('TxKBytes', 0))
            rx = float(json_item.get('RxKBytes', 0))

            self.add(id_, "tx", tx, host_)
            self.add(id_, "rx", rx, host_)

    def add(self, label, direction, value, host=None):
        # Gets the timestamp of the current round
        ns = self.current_scrape

        # --- WAN DEVIATION ---
        if host == "Wan":
            rate_label = f"{label}_{direction}_rate"
            sum_label = f"{label}_{direction}_sum"
            count_label = f"{label}_{direction}_count"

            if rate_label in self.timestamps:
                delta_time = ns - self.timestamps[rate_label]
                estimated_traffic = value * delta_time
            else:
                estimated_traffic = 0

            # Update Rate (Speed)
            self.values[rate_label] = value
            self.timestamps[rate_label] = ns
            self.hosts[rate_label] = host
            self.directions[rate_label] = direction

            # Update Sum (Total accumulated)
            self.values[sum_label] = self.values.get(sum_label, 0) + estimated_traffic
            self.timestamps[sum_label] = ns
            self.hosts[sum_label] = host
            self.directions[sum_label] = direction

            # Update Count (Exact traffic in this interval)
            self.values[count_label] = estimated_traffic
            self.timestamps[count_label] = ns
            self.hosts[count_label] = host
            self.directions[count_label] = direction

            return

        # --- LAN LOGIC ---
        sum_ = f"{label}_{direction}_sum"
        count_ = f"{label}_{direction}_count"
        rate_ = f"{label}_{direction}_rate"

        value_ = self.values.get(sum_)

        if value_ is None:
            # First reading of the device
            self.values[count_] = 0
            self.values[sum_] = value
            self.values[rate_] = 0.0

            self.timestamps[sum_] = ns
            self.timestamps[count_] = ns
            self.timestamps[rate_] = ns

            # Tag host and direction in all three variables
            for l in [sum_, count_, rate_]:
                self.hosts[l] = host
                self.directions[l] = direction
        else:
            if value == value_:
                # Value hasn't changed, exit function without updating date!
                return
            else:
                # Router updated the data
                delta_time = ns - self.timestamps.get(sum_, ns)

                # Delta between old and new reading
                self.values[count_] = value - value_

                if delta_time > 0:
                    self.values[rate_] = (value - value_) / delta_time
                else:
                    self.values[rate_] = 0.0

                self.values[sum_] = value

                # Update timestamp since there was traffic
                self.timestamps[sum_] = ns
                self.timestamps[count_] = ns
                self.timestamps[rate_] = ns

    def format(self):
        result = []
        for label, value in self.values.items():
            host_ = self.hosts[label]
            direction_ = self.directions[label]
            if label.endswith("_rate"):
                result.append(f'#HELP {self.name} {self.description} - gauge')
                result.append(
                    f'huawei_{self.name}_rate{{host="{host_}", direction="{direction_}", unit="Kbps"}} {value * 8}')
            elif label.endswith("_count"):
                result.append(f'#HELP {self.name} {self.description} - counter')
                result.append(
                    f'huawei_{self.name}_count{{host="{host_}", direction="{direction_}",unit="KBytes"}} {value}')
            else:
                result.append(f'#HELP {self.name} {self.description} - sum')
                result.append(
                    f'huawei_{self.name}_sum{{host="{host_}", direction="{direction_}",unit="KBytes"}} {value}')
        result = '\n'.join(result)
        return result

    def format_as_json(self):
        # Exact time of this batch of metrics (maintaining UTC standard)
        now = datetime.datetime.now(datetime.timezone.utc)

        # Temporary dictionary to group things
        grouped_data = {}

        for label, value in self.values.items():
            # FILTER: Only get metrics stamped in the current round
            if self.timestamps.get(label) != getattr(self, 'current_scrape', 0):
                continue

            # Get host and direction (tx or rx)
            host_ = self.hosts.get(label, "Unknown")
            direction_ = self.directions.get(label, "")

            # If the host is not in our dictionary yet, create a space for it
            if host_ not in grouped_data:
                grouped_data[host_] = {}

            # Set the key name that will be inside the JSON and adjust math
            if label.endswith("_rate"):
                key = f"{direction_}_rate_kbps"
                val = value * 8
            elif label.endswith("_count"):
                key = f"{direction_}_interval_traffic_kb"
                val = value
            else:
                key = f"{direction_}_total_accumulated_kb"
                val = value

            # Put the data inside the host's dictionary
            grouped_data[host_][key] = val

        # Transform this group into an array of dictionaries for insertion
        result = []
        for host, data_dict in grouped_data.items():
            if data_dict:  # Ensures empty hosts aren't sent
                result.append({
                    "timestamp": now,
                    "host": host,
                    # json.dumps generates the string for the 'data' column
                    "data": json.dumps(data_dict)
                })

        return result