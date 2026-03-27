import json
import logging
import os
import clickhouse_connect


class ClickHouseDb:
    def __init__(self, host=None, port=None, username=None, password=None):
        self.logger = logging.getLogger()
        self.host = host or os.getenv("CH_HOST", "localhost")
        self.port = port or int(os.getenv("CH_PORT", 8123))
        self.username = username or os.getenv("CH_USER", "admin")
        self.password = password or os.getenv("CH_PASS", "admin")
        self.database = os.getenv("CH_DB", "default")

        self.init_db()

    def get_ch_client(self):
        return clickhouse_connect.get_client(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
        )

    def init_db(self):
        try:
            _client = self.get_ch_client()

            _client.command("""
            CREATE TABLE IF NOT EXISTS network_metrics (
                timestamp DateTime64(3, 'UTC') DEFAULT now64(3, 'UTC') CODEC(DoubleDelta, ZSTD(1)),
                host String CODEC(ZSTD(3)),
                dados String CODEC(ZSTD(9))
            ) ENGINE = MergeTree()
            ORDER BY (host, timestamp)
            """)

            _client.close()
        except Exception as e:
            logging.error(f"Falha ao inicializar banco: {e}")


    def save_network_metrics(self, metrics_list):
        try:
            _client = self.get_ch_client()

            rows = []
            for m in metrics_list:
                rows.append([
                    m["timestamp"],
                    m["host"],
                    m["dados"]
                ])

            _client.insert(
                "network_metrics",
                rows,
                column_names=["timestamp", "host", "dados"],
            )
            _client.close()
        except Exception as e:
            logging.error(f"Falha ao salvar métricas de rede: {e}")