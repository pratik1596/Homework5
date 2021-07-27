import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'teamsData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Pratik'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM teamsData.mlb_teams order by team')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, teams=result)


@app.route('/view/<int:team_id>', methods=['GET'])
def record_view(team_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM teamsData.mlb_teams WHERE id=%s', team_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', team=result[0])


@app.route('/edit/<int:team_id>', methods=['GET'])
def form_edit_get(team_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM teamsData.mlb_teams WHERE id=%s', team_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', team=result[0])


@app.route('/edit/<int:team_id>', methods=['POST'])
def form_update_post(team_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Team'), request.form.get('Payroll_millions'), request.form.get('Wins'), team_id)
    sql_update_query = """UPDATE teamsData.mlb_teams SET Team = %s, Payroll_millions = %s, Wins = %s WHERE id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/team/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Team Form')


@app.route('/team/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Team'), request.form.get('Payroll_millions'), request.form.get('Wins'))
    sql_insert_query = """INSERT INTO teamsData.mlb_teams (Team,Payroll_millions,Wins) VALUES (%s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:team_id>', methods=['POST'])
def form_delete_post(team_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM teamsData.mlb_teams WHERE id = %s """
    cursor.execute(sql_delete_query, team_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM teamsData.mlb_teams')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM teamsData.mlb_teams WHERE id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')