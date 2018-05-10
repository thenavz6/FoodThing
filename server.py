# Code adapted from http://flask.pocoo.org/docs/0.12/patterns/sqlite3/

import sqlite3
from flask import *

app = Flask(__name__)

DATABASE = 'database.db'


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY NOT NULL, fullname TEXT, imageurl TEXT, token TEXT)')
    db.commit()
    db.close()


# Updates a user in the database or creates a new user if not existent
# TODO parse out bad input
def update_user_db(email, name, imageurl, token):
    if (check_user_db(email) == 0):
        db = sqlite3.connect(DATABASE)
        db.execute('INSERT INTO users VALUES ("'+email+'","'+name+'","'+imageurl+'","'+token+'");')
        db.commit()
        db.close() 
    else:
        # Update the token later
        pass


# Returns 1 if this user already exists in the database otherwise returns 0
def check_user_db(email):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('SELECT * from users where email="'+email+'";');
    a = c.fetchall()
    return len(a)


def filter_bad_input(data):
    return data.translate(None, '();')


init_db()
