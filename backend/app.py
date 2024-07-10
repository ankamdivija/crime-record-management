from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def hello() :
    return 'Hey!'

@app.route('/home')
def dashboard() :
    
    return render_template('index.html')


@app.route('/home/<msg>')
def dashboard_msg(msg) :
    
    return render_template('index.html', message=' '.join(msg.split('_')))


@app.route('/search')
def search() :
    
    return render_template('search.html')


@app.route('/search', methods=['POST'])
def search_post() :
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost/CRM") 
    cur = conn.cursor()
    
    # incident_id = request.form['IncidentID']
    field1 = request.form['WeaponCode']

    search_sql = "select * from incident where weapon_code = '{0}';".format(field1)
    
    cur.execute(search_sql)

    data  = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return render_template('/search.html', data=data, query=search_sql)

@app.route('/records/incident')
def records_incident() :
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost/CRM") 
    # Open a cursor to perform database operations
    cur = conn.cursor()

    q1 = "SELECT * FROM incident order by incident_id"
    # Execute a query
    cur.execute(q1)

    incident_data = cur.fetchall()

    return render_template('records_incident.html', data=[incident_data], queries = [q1])

@app.route('/records/victim')
def records_victim() :
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost/CRM") 
    # Open a cursor to perform database operations
    cur = conn.cursor()

    q2 = "SELECT * FROM victim order by victim_id"
    # Execute a query
    cur.execute(q2)

    victim_data = cur.fetchall()

    return render_template('records_victim.html', data=[victim_data], queries = [q2])

@app.route('/records/pemise')
def records_pemise() :
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost/CRM") 
    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    q4 = "SELECT * FROM premise order by premise_code"
    # Execute a query
    cur.execute(q4)

    premise_data = cur.fetchall()

    return render_template('records_premise.html', data=[premise_data], queries = [q4])


@app.route('/records/crimeType')
def records_crimeType() :
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost/CRM") 
    # Open a cursor to perform database operations
    cur = conn.cursor()

    q3 = "SELECT * FROM crime_list"
    # Execute a query
    cur.execute(q3)

    crime_data = cur.fetchall()

    return render_template('records_crime.html', data=[crime_data], queries = [q3])


@app.route('/records/status')
def records_status() :
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost/CRM") 
    # Open a cursor to perform database operations
    cur = conn.cursor()

    q5 = "SELECT * FROM status order by status_code"
    
    cur.execute(q5)

    status_data = cur.fetchall()

    return render_template('records_status.html', data=[status_data], queries = [q5])

@app.route('/report')
def report() :
    return render_template('report.html')

@app.route('/analytics')
def analytics() :
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost/CRM") 
    cur = conn.cursor()

    cur.execute("SELECT cl.status_description, COUNT(*) FROM incident i JOIN status cl ON cl.status_code = i.status_code GROUP BY cl.status_description order by count(*) desc")
    
    query_results = cur.fetchall()
    
    labels = [result[0] for result in query_results]
    values = [result[1] for result in query_results]

    cur.execute("SELECT cl.crime_description, COUNT(*) FROM incident i JOIN crime_list cl ON cl.crime_code = i.crime_code GROUP BY cl.crime_description having count(*) > 100 order by count(*) desc")

    crime_data = [{'crime_code': row[0].split('-')[0] + row[0].split('-')[1].split(' ')[1] if len(row[0].split('-')) > 1 else row[0].split('-')[0], 'value': row[1]} for row in cur.fetchall()]

    return render_template('analytics.html', stats=[crime_data], labels=labels, values=values)

@app.route('/updateIncident', methods=['POST'])
def updateStatus() : 
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost/CRM") 
    cur = conn.cursor()
    
    incident_id = request.form['IncidentID']
    field1 = request.form['WeaponCode']
    update_sql = """
    UPDATE incident
    SET weapon_code = %s
    WHERE incident_id = %s;
    """
    cur.execute(update_sql, (field1, incident_id))

    conn.commit()
    cur.close()
    conn.close()
    return redirect('/home/Your_Update_Is_Successfull')


@app.route('/deleteIncident', methods=['POST'])
def deleteIncident() : 
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost/CRM") 
    cur = conn.cursor()
    
    incident_id = request.form['IncidentID']
    delete_sql = """
    delete from incident
    WHERE incident_id = %s;
    """
    cur.execute(delete_sql, (incident_id,))

    conn.commit()
    cur.close()
    conn.close()
    return redirect('/home/Your_delete_Is_Successfull')


@app.route('/insertIncident', methods=['POST'])
def insertIncident() : 
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost/CRM") 
    cur = conn.cursor()
    
    incident_id = request.form['incident_id']
    field1 = request.form['weapon_code']
    datOcc = request.form['date_occured']
    insert_sql = """
    insert into incident (incident_id, date_occured, weapon_code)
    values(%s, %s, %s);
    """
    cur.execute(insert_sql, (incident_id,datOcc, field1))

    conn.commit()
    cur.close()
    conn.close()
    return redirect('/home/Your_Insert_Is_Successfull')

if __name__ == '__main__':
    app.run()
