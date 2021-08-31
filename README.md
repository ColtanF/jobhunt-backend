# JobHunt (Backend)

This repo is for the backend to my JobHunt React project. JobHunt is a site used for tracking job postings that a user is interested in across all sorts of job listing websites. This backend repo handles interactions between users on the front end and the MySQL DB on the backend.

The backend has a relatively simple architecture. It consists of a Python Flask app that listens for certain API routes and either processes data received on those routes or returns data based on the route accessed, often times both.

The routes are straightforward in the main Flask app.py file: /jobs will allow you to access the list of saved jobs, /job/add_job will allow users to add jobs, etc.

### If I wanted to use this, what would I need to do?

You could start by checking out the code from this repo. Besides that, you'll need MySQL, Python (I used v3, but you could probably use v2 if you wanted, with a bit of retooling), pip, and several Python packages. The full list is in the requirements.txt file at the root of the project. You can use the following command within a Python virtual environment (or just on your computer if you want all of the packages for your global Python installation) to install all of the packages you need:

```
pip install -r requirements.txt
```

Once you have all of that, you'll need to set up your MySQL installation (if you haven't already) and add a database to use for this project. You can either modify the code directly to contain your database info (earlier versions of the code did this for my local MySQL DB), but in the current version of the code, I actually pull from an environment variable on my system that contains all of the database info. If you go the environment variable route, you'll need to add an env variable called "DATABASE_URL" that contains the following structure:

```
mysql://<mysql db username>:<mysql db password>@<mysql db host address (localhost if local)>/<database name>
```

The code in mysql_db_helper.py should take care of setting up the tables you'll need, although the authentication tables aren't working yet. As a result, all of the records are currently being saved with the same username, but that will be fixed in the future when authentication is fully working.
