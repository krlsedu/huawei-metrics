# Huawei AX3 Pro Prometheus Exporter

[![Python 3.9.13](https://img.shields.io/badge/python-3.9.13-blue.svg)](https://www.python.org/downloads/release/python-3913/)

## Description

This project is a Prometheus exporter for Huawei, specifically designed and tested for AX3 Pro routers. It uses Selenium
with PhantomJS for authentication and interaction with the router's APIs. The exporter is ready for use with Docker
through the project's Dockerfile. This is in the initial development stage and refining is still needed.

Environment variables are used for configuration:

* `HUAWEI_HOST`: Set this to the URL of your router.
* `HUAWEI_USER`: Set this to the username.
* `HUAWEI_PASSWORD`: Set this to the password.

### Known Issues

1) If data is fetched at very short intervals (i.e., less than 10 seconds), the data is not updated.
2) Even if the update frequency is every 30 seconds, a zero-read occurs every 5 minutes. This issue is under
   investigation.
3) A more elegant method of connecting and authorizing is needed - this project is currently still in the POC (proof of
   concept) stage.
4) A more elegant method to generate the metrics

## Prerequisites

Ensure you have Python version 3.9.13 and pip, the Python package installer.

## Installation

To install necessary packages, run:

```bash
pip install -r requirements.txt
```

## Building Docker Image

The Dockerfile for this project is included. To build a Docker image, use the following command:

```bash
docker build -t huawei-prometheus-exporter .
```
the base image is krlsedu/csctracker-ubuntu:latest
from the following project:
https://github.com/krlsedu/CscTrackerUbuntu
is based on ubuntu 20.04 for compatibilite with phantomjs and includes the following packages:
1) python3.9
2) python3-pip
3) phantomjs


## Docker Execution

You can run the Docker image as follows, replacing `<env>` with your actual environment variables:

```bash
docker run -e HUAWEI_HOST=  -e HUAWEI_USER=  -e HUAWEI_PASSWORD=  huawei-prometheus-exporter
```
or
```bash
docker compose up -d
```

## Usage

To use this exporter, you need to add the following to your Prometheus configuration:

```yaml
  - job_name: 'Huawei exporter'
    metrics_path: '/prometheus-metrics'
    scrape_interval: 30s
    static_configs:
      - targets: [ 'huawei_metrics:5000' ]
```

## Metrics

metrics are available at the following endpoint: `/prometheus-metrics`
example:

```text
#HELP network_traffic Network traffic - counter
huawei_network_traffic_count{host="Host_name", direction="tx",unit="KBytes"} 70821.0
#HELP network_traffic Network traffic - sum
huawei_network_traffic_sum{host="Host_name", direction="tx",unit="KBytes"} 1844131.0
#HELP network_traffic Network traffic - gauge
huawei_network_traffic_rate{host="Host_name", direction="tx", unit="Kbps"} 3585.8734177215188
#HELP network_traffic Network traffic - counter
huawei_network_traffic_count{host="Host_name", direction="rx",unit="KBytes"} 9739.0
#HELP network_traffic Network traffic - sum
huawei_network_traffic_sum{host="Host_name", direction="rx",unit="KBytes"} 6139978.0
#HELP network_traffic Network traffic - gauge
huawei_network_traffic_rate{host="Host_name", direction="rx", unit="Kbps"} 493.11392405063293
```

## Grafana Dashboard
Import the dashboard from the file `grafana_dashboard.json` into your Grafana instance.

in the dashboard, you can see the following metrics:
1) Internet usage in Kbps - obtained from the router's API whith the following project:
https://github.com/krlsedu/dd-wrt-prometheus-exporter adapted from the following project:
https://github.com/Enrico204/dd-wrt-prometheus-exporter

2) Local network usage in Kbps - obtained from the router's API whith this project.
3) Local network usage in Kbps by hosts - obtained from the router's API whith this project.
4) Total traffic download in KBytes by hosts - obtained from the router's API whith this project.
5) Total traffic upload in KBytes by hosts - obtained from the router's API whith this project.
6) Total traffic in KBytes - obtained from the router's API whith this project.

## Help

If you have any questions or encountered any issues, feel free to open an issue in this repository.

## Authors

Your Name here

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
