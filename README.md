# Huawei AX3 Pro Prometheus Exporter

[![Python 3.9.13](https://img.shields.io/badge/python-3.9.13-blue.svg)](https://www.python.org/downloads/release/python-3913/)

## Description

This project is a Prometheus exporter for Huawei routers, specifically designed and tested for the AX3 Pro model. It collects network traffic metrics (LAN and WAN) and exposes them in Prometheus format.

The exporter can also run a background task to periodically save metrics into a ClickHouse database.

## Features

- **Prometheus Metrics**: Exposes real-time traffic data for all connected devices and the WAN interface.
- **ClickHouse Integration**: Optional background task to persist metrics for long-term analysis.
- **Docker Ready**: Easily deployable using Docker or Docker Compose.
- **Automated Authentication**: Uses Selenium with PhantomJS to handle router login and data scraping.

## Configuration

Environment variables are used for configuration:

- `HUAWEI_HOST`: Router IP or hostname (e.g., `192.168.3.1`).
- `HUAWEI_USER`: Router admin username.
- `HUAWEI_PASSWORD`: Router admin password.
- `TIME_SLEEP`: Interval in seconds for the background ClickHouse collection (default: `5`). Set to `0` to disable background collection.
- `CH_HOST`, `CH_PORT`, `CH_USER`, `CH_PASS`, `CH_DB`: ClickHouse connection details.

## API Endpoints

- `GET /prometheus-metrics`: Returns metrics in Prometheus text format.
- `GET /json-metrics`: Returns metrics in JSON format.
- `GET /deviceinfo`: Returns basic router device information.
- `GET /health`: Health check endpoint. Returns `200 OK` if the last scrape was successful.

## Prerequisites

- Python 3.9.13
- PhantomJS (included in the Docker image)

## Installation & Execution

### Local Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```

### Docker

1. Build the image:
   ```bash
   docker build -t huawei-prometheus-exporter .
   ```
2. Run with environment variables:
   ```bash
   docker run -d \
     -e HUAWEI_HOST=192.168.3.1 \
     -e HUAWEI_USER=admin \
     -e HUAWEI_PASSWORD=yourpassword \
     -p 5000:5000 \
     huawei-prometheus-exporter
   ```
   Or use `docker-compose up -d`.

## Prometheus Configuration

Add the following to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'huawei-exporter'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/prometheus-metrics'
    scrape_interval: 30s
```

## Grafana Dashboard

An example dashboard is provided in `grafana_dashboard.json`. It includes:
1. Internet usage (WAN).
2. Local network (LAN) usage.
3. Traffic per host.
4. Total traffic download/upload.

## Known Issues

1. Data may not update if scraped at intervals shorter than 10 seconds.
2. Occasional zero-reads every 5 minutes (under investigation).

## License

MIT License - see the `LICENSE` file for details.
