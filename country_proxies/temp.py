from proxy import Proxy
import requests
import pandas as pd

proxy = {"http": "http://132.226.36.165:3128", "https": "http://45.152.188.214:3128", "ftp": "ftp://10.10.1.10:3128"}
url = "https://www.mcallen.net/departments/bridge/anzalduas"
header = {'User-agent': Proxy.get_random_ua()}
print(requests.get(url, proxies=proxy, headers=header))
