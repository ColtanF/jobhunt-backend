import time
from flask import Flask,jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from passlib.hash import sha256_crypt
import os
import json

app = Flask(__name__)
app.debug = True
CORS(app)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'qwerQWER1234!@#$'
# app.config['MYSQL_DB'] = 'job_tracker_db'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

def get_mysql_environs():
    print(os.environ['DATABASE_URL'])

mysql = MySQL(app)

@app.route('/')
def home():
    return {'home': 'here'}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/register', methods=["POST"])
def register():

    # get the user fields
    newUser = json.loads(request.data)
    name = newUser['name']
    email = newUser['email']
    username = newUser['username']
    password = sha256_crypt.encrypt(newUser['password'])
    
    # check if the username already exists
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", [newUser['username']])
    mysql.connection.commit()
    data = cur.fetchall()
    if len(data) != 0: 
        response = jsonify(error= 'User account for ' + newUser['username'] + ' already exists!')
        return response
    # add the user to the users table
    cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
    mysql.connection.commit()
    cur.close()
    response = jsonify(response=200,user="registered")
    return response

@app.route('/login', methods=["POST"])
def login():
    # grab the login info
    userInfo = json.loads(request.data)
    username = userInfo["username"]
    password_candidate = userInfo["password"]
    
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE username=%s", [username])
    if result > 0:
        data = cur.fetchone()
        password = data['password']
        cur.close()
        # compare the stored password with the login attempt's password
        if sha256_crypt.verify(password_candidate, password):
            response = jsonify(response=200, logged_in=True)
        else:
            response = jsonify(error="Invalid password. Please try again.")
        return response
    else:
        response = jsonify(error="Invalid username. Please try again.")
        return response

@app.route('/jobs')
def getJobs():
    cur = mysql.connection.cursor()

    # grab all of the jobs
    result = cur.execute("SELECT * FROM jobs_tbl")

    jobs = cur.fetchall()
    cur.close()
    jobs = list(jobs)
    response = jsonify(jobs)

    return response

@app.route('/job/<string:id>')
def getJob(id):
    cur = mysql.connection.cursor()

    # grab all of the jobs
    result = cur.execute("SELECT * FROM jobs_tbl WHERE id = %s", [id])

    jobs = cur.fetchall()
    cur.close()
    jobs = list(jobs)
    response = jsonify(jobs)

    return response

@app.route('/job/add_job', methods=["POST"])
def addJob():
    newJob = json.loads(request.data)
    # print(newJob)
    company = newJob['company']
    position = newJob['position']
    companyInfo = newJob['companyInfo']
    positionInfo = newJob['positionInfo']
    reqsIMeet = newJob['reqsIMeet']
    reqsIDontMeet = newJob['reqsIDontMeet']
    salary = newJob['salary']
    address = newJob['address']
    links = newJob['links']
    status = newJob['status']
    statusNotes = newJob['statusNotes']
    username = 'Coltan66'
     # Add the job to the DB
    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO jobs_tbl(company, position, companyInfo, positionInfo, reqsIMeet, reqsIDontMeet, salary, address, links, status, statusNotes, username, rating, rejected) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0, false)",
                (company, position, companyInfo, positionInfo, reqsIMeet, reqsIDontMeet, salary, address, links, status, statusNotes, username))

    mysql.connection.commit()
    cur.close()

    response = jsonify(response=200,record="added")
    return response

    
@app.route('/job/edit_job/<string:id>', methods=["POST"])
def editJob(id):
    editJob = json.loads(request.data)
    # print(editJob)
    company = editJob['company']
    position = editJob['position']
    companyInfo = editJob['companyInfo']
    positionInfo = editJob['positionInfo']
    reqsIMeet = editJob['reqsIMeet']
    reqsIDontMeet = editJob['reqsIDontMeet']
    salary = editJob['salary']
    address = editJob['address']
    links = editJob['links']
    status = editJob['status']
    statusNotes = editJob['statusNotes']
     # Add the job to the DB
    cur = mysql.connection.cursor()

    cur.execute("UPDATE jobs_tbl SET company = %s, position = %s, companyInfo = %s, positionInfo = %s, reqsIMeet = %s, reqsIDontMeet = %s, salary = %s, address = %s, links = %s, status = %s, statusNotes = %s WHERE id = %s",
                (company, position, companyInfo, positionInfo, reqsIMeet, reqsIDontMeet, salary, address, links, status, statusNotes, id))
    mysql.connection.commit()
    cur.close()

    response = jsonify(response=200,record="modified")
    return response


@app.route('/job/delete_job/<string:id>', methods=["POST"])
def deleteJob(id):
    cur = mysql.connection.cursor()
    result = cur.execute("DELETE FROM jobs_tbl WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    response = jsonify(response=200, record="deleted")
    return response

@app.route('/job/update_rating/<string:id>', methods=["POST"])
def updateRating(id):
    rating = json.loads(request.data)

    cur = mysql.connection.cursor()
    result = cur.execute("UPDATE jobs_tbl SET rating = %s WHERE id = %s", [rating['rating'], id])
    # print(result)
    mysql.connection.commit()
    cur.close()

    response = jsonify(response=200, rating="updated")
    return response

if __name__ == "__main__":
    app.secret_key = "123abc"
    get_mysql_environs()
    app.run(port=5000)
