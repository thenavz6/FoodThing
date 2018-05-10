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
# TODO parse out bad input TODO check the token with Google
def update_user_db(email, name, imageurl, token):
    if (check_user_db(email) == 0):
        db = sqlite3.connect(DATABASE)
        db.execute('INSERT INTO users VALUES ("'+email+'","'+name+'","'+imageurl+'","'+token+'");')
    else:
        db = sqlite3.connect(DATABASE)
        db.execute('UPDATE users SET token = "'+token+'" WHERE email="'+email+'";')
    db.commit()
    db.close()


# Returns 1 if this user already exists in the database otherwise returns 0
def check_user_db(email):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('SELECT * from users where email="'+email+'";')
    a = c.fetchall()
    return len(a)


# Returns 1 if the current token associated to this email matches the argument token
def compare_token_db(email, token):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('SELECT * from users where email="'+email+'";')
    a = c.fetchone()
    if a == None or a[3] != token:
        return 0
    return 1


def filter_bad_input(data):
    return data.translate(None, '();')


init_db()
