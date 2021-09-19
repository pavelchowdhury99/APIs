from flask import Flask, jsonify, make_response
from proxy import Proxy
import multiprocessing
import sqlite3
import time
import yaml
import random

app = Flask(__name__)


def activate():
    print("Inside activate")
    while 1:
        conn = sqlite3.connect("Proxy.db")
        cursor = conn.cursor()
        x = Proxy(country_code='us', config_yaml_path='config.yaml')
        x.run(context={'cursor': cursor})
        # x.update_proxies(proxies={'http': 'http://98.116.152.143:3128', 'https': 'http://20.69.69.212:3128'}, context={'cursor': cursor})
        # print(x.get_country_proxies_from_db(context={'cursor': cursor}))
        # x.extract_new_proxies()
        conn.commit()
        conn.close()
        time.sleep(15)


@app.route('/')
def home():
    conn = sqlite3.connect("Proxy.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNTRY,HTTP, HTTPS
                    FROM PROXY
                    WHERE COUNTRY='US';
                    ''')
    result = cursor.fetchall()[0]
    with open('config.yaml') as f:
        list_ = yaml.safe_load(f).get('USER_AGENTS')
    response = {result[0]: {'http': result[1], 'https': result[2]}, 'RANDOM_USER_AGENT': random.choice(list_), 'USER_AGENTS':list_}
    # conn.commit()
    conn.close()
    return jsonify(response)

def API():
    print('In API')
    app.run(debug=True)


if __name__ == '__main__':
    # p = multiprocessing.Process(target=API, args=())
    p = multiprocessing.Process(target=API)
    p.start()
    time.sleep(3)
    print('After Flask run')
    activate()
