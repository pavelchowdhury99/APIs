from country_proxies.common import read_yaml, get_logger
import sys
from timeit import timeit
import requests
import pandas as pd
import yaml
import os
from bs4 import BeautifulSoup
import logging
import json
import random

logger = get_logger()


class Proxy:

    def __init__(self, country_code, config_yaml_path, context):
        self.config = read_yaml(config_yaml_path)['PROXY_WEBSITES'][country_code.upper()]
        self.config_yaml_path = config_yaml_path
        self.context = context

    def get_random_ua(self):
        user_agents = read_yaml(self.config_yaml_path).get('USER_AGENTS')
        return user_agents[random.randint(0, len(user_agents) - 1)]

    def check_proxy_workings(self, proxy_dict, url_to_check):
        """
        Static function to check if a proxy is working or not
        Returns True/False
        """
        try:
            header = {'User-agent': self.get_random_ua()}
            if requests.get(url_to_check, proxies=proxy_dict, headers=header, timeout=200).ok:
                return True
        except:
            return False

    def update_proxies(self):
        # with open(read_yaml('config.yaml')['PROXY_DATAFRAME']['PATH']) as f:
        #     d = json.load(f)
        #     print(d)
        pass

    def extract_proxies(self):
        """
        Fetch proxies from website and return a dictionary
        This function needs to be overwritten country to country
        """
        # reading website for proxies
        proxy_website = self.config.get('PROXY_SITE')

        # reading page table into DataFrame
        df = pd.read_html(requests.get(proxy_website, timeout=200).text)[0]

        # separating http and https proxies
        df_http = df[df['Https'] == 'no']
        df_https = df[df['Https'] == 'yes']
        proxy_dict = {}

        # fetching proxy for http url
        http_test_url = self.config.get("HTTP_TEST")
        for count, proxy in enumerate(df_http.iterrows()):
            proxy_dict["http"] = f"http://{proxy[1]['IP Address']}:{int(proxy[1]['Port'])}"
            if self.check_proxy_workings(proxy_dict=proxy_dict, url_to_check=http_test_url):
                logger.info(f'Proxy {proxy_dict} has worked for http')
                break
            else:
                logger.info(f'Proxy {count} failed')

        # fetching proxy for https url
        https_test_url = self.config.get("HTTPS_TEST")
        for count, proxy in enumerate(df_https.iterrows()):
            proxy_dict["https"] = f"http://{proxy[1]['IP Address']}:{int(proxy[1]['Port'])}"
            if self.check_proxy_workings(proxy_dict=proxy_dict, url_to_check=https_test_url):
                logger.info(f'Proxy {proxy_dict} has worked for https')
                break
            else:
                logger.info(f'Proxy {count} failed {proxy_dict}')


if __name__ == "__main__":
    x = Proxy(country_code='us', config_yaml_path='config.yaml', context={})
    x.extract_proxies()
    # x.update_proxies()
    # print(x.context)
