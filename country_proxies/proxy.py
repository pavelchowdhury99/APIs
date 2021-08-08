from country_proxies.common import read_yaml
import requests
import pandas as pd
import yaml
import os
from bs4 import BeautifulSoup


class Proxy:

    def __init__(self, country_code, config_yaml_path, context):
        self.config = read_yaml(config_yaml_path)['PROXY_WEBSITES'][country_code.upper()]
        self.context = context

    def extract_proxies(self):
        '''
        Fetch proxies from website and return a dictionary
        This fucntion needs to be overwritten country to country
        '''
        # reading website for proxies
        proxy_website = self.config.get('PROXY_SITE')
        print(proxy_website)
        # reading page table into DataFrame
        df = pd.read_html(requests.get(proxy_website, timeout=200).text)
        http_test_site = self.config.get('HTTP_TEST')
        https_test_site = self.config.get('HTTPS_TEST')
        print(http_test_site, https_test_site)


if __name__ == "__main__":
    x = Proxy(country_code='us', config_yaml_path='config.yaml', context={})
    x.extract_proxies()
    # print(x.context)
