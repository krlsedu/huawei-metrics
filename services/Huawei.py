import os
import platform

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from services.Metrics import PrometheusMetric

BASE_URL = "http://{host}"

metrics_network = PrometheusMetric("network_traffic", "Network traffic")


class Ax3Pro:
    def __init__(self, host=None, user=None, password=None):

        self.browser = None
        self.session = None
        self.base_url = None

        if host is None:
            host = os.environ['HUAWEI_HOST']
        self.host = host

        if user is None:
            user = os.environ['HUAWEI_USER']
        self.user = user

        if password is None:
            password = os.environ['HUAWEI_PASSWORD']
        self.password = password

        self.connect()

    def connect(self):
        self.base_url = BASE_URL.format(host=self.host)
        self.session = requests.Session()

        if platform.system() == "Windows":
            phantomjs_path = "./phantomjs.exe"
        else:
            phantomjs_path = "phantomjs"

        self.browser = webdriver.PhantomJS(phantomjs_path)
        self.browser.get(self.base_url)
        self.login()

    def login(self):
        try:
            elem = self.browser.find_element_by_id("userpassword_ctrl")
            elem.clear()
            elem.send_keys(self.password)

            elem = self.browser.find_element_by_id("loginbtn")
            elem.click()
        except Exception as e:
            print(e)
            self.login()
            pass

    def scrape(self, path):
        self.browser.execute_script('window.localStorage.clear();')
        self.browser.get(self.base_url + "/html/index.html#/devicecontrol")

        url = self.browser.current_url

        if "login" in url:
            self.login()

        self.browser.get(self.base_url + path)
        pg = self.browser.page_source
        soup = BeautifulSoup(pg, 'html.parser')
        pg = soup.find_all('body')[0].text

        metrics_network.to_metric(pg)

        return metrics_network.format()
