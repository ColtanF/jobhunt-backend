#! python3
''' 
    Purpose: This python code will be run when running the JobHunt Python app.  
    Essentially, the code in this file will check for the existence of MySQL,
    the MySQL database used for JobHunt issue tracking, and the table(s) used in 
    said DB. 

    If MySQL does exist, but he DB/table(s) do not, this script will attempt
    to initialize them
'''

import mysql.connector
import os
import urllib.parse

urllib.parse.uses_netloc.append('mysql')

dbs = {}


tables = {}
tables['jobs_tbl'] = (
    "CREATE TABLE jobs_tbl(" +
    "  id INT(11) AUTO_INCREMENT PRIMARY KEY," +
    "  company VARCHAR(100)," +
    "  position VARCHAR(200)," +
    "  companyInfo TEXT," + 
    "  positionInfo TEXT," + 
    "  reqsIMeet TEXT," + 
    "  reqsIDontMeet TEXT," + 
    "  salary varchar(200)," + 
    "  address VARCHAR(200)," +
    "  links TEXT," +
    "  status VARCHAR(200)," +
    "  rating INT," +  
    "  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
)

def checkAndMakeDB():
    db = ""
    hostname = ""
    username = ""
    password = ""

    if 'CLEARDB_DATABASE_URL' in os.environ or "DATABASE_URL" in os.environ:        
        url={}
        if 'CLEARDB_DATABASE_URL' in os.environ:
            url = urllib.parse.urlparse(os.environ['CLEARDB_DATABASE_URL'])
        else:
            url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
        db = url.path[1:]
        dbs[db] = ("CREATE DATABASE " + db + ";")
        hostname = url.hostname
        username = url.username
        password = url.password

    db_connection = mysql.connector.connect(
        host=hostname, # replace with wherever you host your db
        user=username, # replace with your username
        password=password # replace with a real password
    )
    db_cursor = db_connection.cursor()

    print("db value = " + db)
    db_cursor.execute("SHOW DATABASES;")
    databases = [item[0] for item in db_cursor.fetchall()]

    for key in dbs:
        if key in databases:
            print("Found " + key + " database!")
        else:
            print("Database " + key + " not found. Creating new database...")
            #db_cursor.execute(dbs[key])
        
    # If I ever used more than one DB for some reason, would need to update
    #  hard coded values here and in the for loop below...
    db_cursor.execute("SHOW TABLES in " + db + ";")

    dbTables = [item[0] for item in db_cursor.fetchall()]

    for key in tables:
        if key in dbTables:
            print("Found " + key + "!")
        else:
            print(key + " not found. Creating table...")
            db_cursor.execute("USE "+db+";")
            db_cursor.execute(tables[key])

    db_cursor.close()
