from flask import Flask
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    conn = sqlite3.connect("Proxy.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNTRY,HTTP, HTTPS
                    FROM PROXY
                    WHERE COUNTRY='US';
                    ''')
    result = cursor.fetchall()[0]
    response = {result[0]: {'http': result[1], 'https': result[2]}}
    conn.commit()
    conn.close()
    return response


if __name__ == '__main__':
    app.run(debug=True)
