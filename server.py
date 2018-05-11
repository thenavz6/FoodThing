# Code adapted from http://flask.pocoo.org/docs/0.12/patterns/sqlite3/

import sqlite3
from flask import *

app = Flask(__name__)

DATABASE = 'database.db'


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY NOT NULL, fullname TEXT, imageurl TEXT, token TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_overview (recipeID TEXT PRIMARY KEY NOT NULL, recipeLabel TEXT, recipeImageLink Text)')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_keywords (recipeID TEXT, keyword TEXT, FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID))')
    db.commit()
    db.close()


# Updates a user in the database or creates a new user if not existent
# TODO parse out bad input TODO check the token with Google
def update_user_db(email, name, imageurl, token):
    try:
        db = sqlite3.connect(DATABASE)
        db.execute('INSERT INTO users VALUES ("'+email+'","'+name+'","'+imageurl+'","'+token+'");')
    except sqlite3.IntegrityError as e:
        print("User already in database")
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
    db.close()
    return len(a)


# Returns 1 if the current token associated to this email matches the argument token
def compare_token_db(email, token):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('SELECT * from users where email="'+email+'";')
    a = c.fetchone()
    db.close()
    if a == None or a[3] != token:
        return 0
    return 1


# Adds a new recipe overview entry and also recipe_keyword entries
def add_recipe_overview_db(recipeId, label, urllink):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    try:
        c.execute('INSERT INTO recipe_overview VALUES ("'+recipeId+'","'+label+'","'+urllink+'");')
        for word in label.split(" "):
            add_recipe_keyword(c, recipeId, word)
    except sqlite3.IntegrityError as e:
        print("Recipe already in database")
    
    db.commit()
    db.close()


def add_recipe_keyword(cursor, recipeId, word):
    cursor.execute('INSERT INTO recipe_keywords VALUES ("'+recipeId+'","'+word+'");')


# Return recipes that have a matching keyword in the recipe_keywords table
def find_recipes_keyword(word):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('SELECT * from recipe_keywords where keyword="'+word+'";')
    hits = c.fetchall()
    for hit in hits:
        print(hit[0])
    
    db.close()


def find_recipe_id(cursor, recipeId):
    cursor.execute('SELECT * from recipe_overview where recipeID="'+recipeId+'";')


def filter_bad_input(data):
    return data.translate(None, '();')


init_db()
