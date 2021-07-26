from typing import List, Dict
import mysql.connector
import simplejson as json
from flask import Flask, Response

app = Flask(__name__)


def teams_import() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'teamsData'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM mlb_teams')
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


@app.route('/')
def index() -> str:
    js = json.dumps(teams_import())
    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')