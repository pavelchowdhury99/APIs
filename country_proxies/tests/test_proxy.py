import os
import pytest
import yaml
import requests
from country_proxies.common import read_yaml


def test_us_proxy_site():
    url = read_yaml(os.path.join(os.pardir, 'config.yaml'))['PROXY_WEBSITES']['US']
    assert requests.get(url).ok == True, "URL of us proxies is having error"


if __name__ == "__main__":
    pytest.main(['-v'])
