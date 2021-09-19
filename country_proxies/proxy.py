from country_proxies.common import read_yaml, get_logger
import time
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
import sqlite3

logger = get_logger()


class Proxy:

    def __init__(self, country_code, config_yaml_path):
        self.country_code = country_code.upper()
        self.config = read_yaml(config_yaml_path)['PROXY_WEBSITES'][self.country_code]
        self.config_yaml_path = config_yaml_path

    def get_random_ua(self):
        user_agents = read_yaml(self.config_yaml_path).get('USER_AGENTS')
        return user_agents[random.randint(0, len(user_agents) - 1)]

    def get_country_proxies_from_db(self, context):
        cursor = context.get('cursor')
        query = 'SELECT COUNTRY,HTTP, HTTPS FROM PROXY WHERE COUNTRY= ?;'
        cursor.execute(query, (self.country_code,))
        res = cursor.fetchall()
        if res:
            proxy = {'http': res[0][1], 'https': res[0][2]}
        else:
            proxy = {'http': None, 'https': None}
            logger.info(f"No existing proxies for country {self.country_code}")
        return proxy

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

    def update_proxies(self, proxies, context):
        cursor = context.get('cursor')
        query = "UPDATE PROXY SET HTTP=?, HTTPS=? WHERE COUNTRY = ?;"
        params = (proxies.get('http'), proxies.get('https'), self.country_code)
        cursor.execute(query, params)
        return context

    def extract_new_proxies(self, for_https=False):
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

        if for_https:
            # fetching proxy for https url
            https_test_url = self.config.get("HTTPS_TEST")
            for count, proxy in enumerate(df_https.iterrows()):
                proxy_dict["https"] = f"http://{proxy[1]['IP Address']}:{int(proxy[1]['Port'])}"
                if self.check_proxy_workings(proxy_dict=proxy_dict, url_to_check=https_test_url):
                    logger.info(f'Proxy {proxy_dict} has worked for https')
                    return proxy_dict
                else:
                    logger.info(f'Proxy {count} failed {proxy_dict}')
        else:
            # fetching proxy for http url
            http_test_url = self.config.get("HTTP_TEST")
            for count, proxy in enumerate(df_http.iterrows()):
                proxy_dict["http"] = f"http://{proxy[1]['IP Address']}:{int(proxy[1]['Port'])}"
                if self.check_proxy_workings(proxy_dict=proxy_dict, url_to_check=http_test_url):
                    logger.info(f'Proxy {proxy_dict} has worked for http')
                    return proxy_dict
                else:
                    logger.info(f'Proxy {count} failed')

    def run(self, context):
        proxy = self.get_country_proxies_from_db(context)
        https_test_url = self.config.get("HTTPS_TEST")
        http_test_url = self.config.get("HTTP_TEST")
        # for https
        if self.check_proxy_workings(proxy, https_test_url):
            logger.info("Previous https proxy still working for https")
        else:
            proxy.update(dict(https=self.extract_new_proxies(for_https=True).get('https')))
            logger.info("Updating new proxy for https")
        # for http
        if self.check_proxy_workings(proxy, http_test_url):
            logger.info("Previous http proxy still working for http")
        else:
            proxy.update(dict(http=self.extract_new_proxies(for_https=False).get('https')))
            logger.info("Updating new proxy for http")
        self.update_proxies(proxy, context)
        logger.info("All run successfully")


if __name__ == "__main__":
    while 1:
        conn = sqlite3.connect("Proxy.db")
        cursor = conn.cursor()
        x = Proxy(country_code='us', config_yaml_path='config.yaml')
        x.run(context={'cursor': cursor})
        # x.update_proxies(proxies={'http': 'http://98.116.152.143:3128', 'https': 'http://34.138.225.120:8888'}, context={'cursor': cursor})
        print(x.get_country_proxies_from_db(context={'cursor': cursor}))
        # x.extract_new_proxies()
        conn.commit()
        conn.close()
        time.sleep(15)
