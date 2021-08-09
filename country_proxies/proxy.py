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
        self.context = context

    @staticmethod
    def get_random_ua():
        user_agents = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3) Gecko/20090305 Firefox/3.1b3 GTB5",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; ko; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2",
            "Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.9b5) Gecko/2008032620 Firefox/3.0b5",
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.12) Gecko/20080214 Firefox/2.0.0.12",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8",
            "Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.0.5) Gecko/20060819 Firefox/1.5.0.5",
            "Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3",
            "Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.9) Gecko/20050711 Firefox/1.0.5",
            "Mozilla/5.0 (Windows; Windows NT 6.1; rv:2.0b2) Gecko/20100720 Firefox/4.0b2",
            "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b4) Gecko/20100818 Firefox/4.0b4",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20101111 Firefox/4.0b7",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre",
            "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b9pre) Gecko/20110111 Firefox/4.0b9pre",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre",
            "Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2",
            "Mozilla/5.0 (X11; Linux i686 on x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2",
            "Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0",
            "Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:25.0) Gecko/20100101 Firefox/25.0",
            "Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0",
            "Mozilla/5.0 (X11; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0",
            "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0"
        ]

        return user_agents[random.randint(0, len(user_agents) - 1)]

    @staticmethod
    def check_proxy_workings(proxy_dict, url_to_check):
        """
        Static function to check if a proxy is working or not
        Returns True/False
        """
        try:
            header = {'User-agent': Proxy.get_random_ua()}
            if requests.get(url_to_check, proxies=proxy_dict, headers=header, timeout=200).ok:
                return True
        except:
            return False

    def update_proxies(self):
        with open(read_yaml('config.yaml')['PROXY_DATAFRAME']['PATH']) as f:
            d = json.load(f)
            print(d)

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
            if Proxy.check_proxy_workings(proxy_dict=proxy_dict, url_to_check=http_test_url):
                logger.info(f'Proxy {proxy_dict} has worked for http')
                break
            else:
                logger.info(f'Proxy {count} failed')

        # fetching proxy for https url
        https_test_url = self.config.get("HTTPS_TEST")
        for count, proxy in enumerate(df_https.iterrows()):
            proxy_dict["https"] = f"http://{proxy[1]['IP Address']}:{int(proxy[1]['Port'])}"
            if Proxy.check_proxy_workings(proxy_dict=proxy_dict, url_to_check=https_test_url):
                logger.info(f'Proxy {proxy_dict} has worked for https')
                break
            else:
                logger.info(f'Proxy {count} failed {proxy_dict}')


if __name__ == "__main__":
    x = Proxy(country_code='us', config_yaml_path='config.yaml', context={})
    x.extract_proxies()
    # x.update_proxies()
    # print(x.context)
