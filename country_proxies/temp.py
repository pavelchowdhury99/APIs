# from proxy import Proxy
import requests
import pandas as pd
import sqlite3

# proxy = {"http": "http://132.226.36.165:3128", "https": "http://45.152.188.214:3128", "ftp": "ftp://10.10.1.10:3128"}
# url = "https://www.mcallen.net/departments/bridge/anzalduas"
# header = {'User-agent': Proxy.get_random_ua()}
# print(requests.get(url, proxies=proxy, headers=header))


# # Creating sqlite db and table
# conn = sqlite3.connect("Proxy.db")
# conn.execute('''CREATE TABLE PROXY
#                 ( COUNTRY TEXT PRIMARY KEY,
#                     HTTP TEXT,
#                     HTTPS TEXT
#                 );
#                 ''')
# conn.commit()
# conn.close()

# # Inserting into table
# conn = sqlite3.connect("Proxy.db")
# conn.execute('''INSERT INTO PROXY (COUNTRY,HTTP, HTTPS)
#                 VALUES ('US', 'http://98.116.152.143:3128', 'http://20.69.69.212:3128');
#                 ''')
# conn.commit()
# conn.close()

# # Selecting from table
# conn = sqlite3.connect("Proxy.db")
# cursor = conn.cursor()
# cursor.execute('''SELECT COUNTRY,HTTP, HTTPS
#                 FROM PROXY
#                 WHERE COUNTRY='US';
#                 ''')
# result = cursor.fetchall()[0]
# response = {result[0]: {'http': result[1], 'https': result[2]}}
# print(response)
# conn.commit()
# conn.close()


# import flask
# from flask import request, jsonify, make_response
# import time
# import multiprocessing
#
# app = flask.Flask('__name__')
#
#
# @app.route('/')
# def home():
#     return ({"home": 'home'})
#
#
# def API(Conf):
#     print('In API selction')
#     app.run(debug=True)
#
#
# if __name__ == "__main__":
#     config = {"Something": "SomethingElese"}
#     p = multiprocessing.Process(target=API, args=('a',))
#     p.start()
#     time.sleep(3)
#     print('After Flask run')

# import yaml
# with open('config.yaml') as f:
#     dict_=yaml.safe_load(f).get('USER_AGENTS')
#     print(dict_)

import requests
d = {'http': None, 'https': 'http://34.138.225.120:8888'}
print(requests.get('http://www.ritba.org/tolls-2/', proxies=d).text)
