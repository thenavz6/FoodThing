# Code adapted from http://flask.pocoo.org/docs/0.12/patterns/sqlite3/

import sqlite3
from flask import *

app = Flask(__name__)

DATABASE = 'database.db'


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY NOT NULL, fullname TEXT, imageurl TEXT, token TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_overview (recipeID TEXT PRIMARY KEY NOT NULL, recipeLabel TEXT, recipeImageLink TEXT, recipeRating REAL)')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_keywords (recipeID TEXT, keyword TEXT, FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID))')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_comments (recipeID TEXT, comment TEXT, username TEXT, userimage TEXT, FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID))')
    db.commit()
    db.close()


# Updates a user in the database or creates a new user if not existent
# TODO parse out bad input TODO check the token with Google
def update_user_db(email, name, imageurl, token):
    try:
        db = sqlite3.connect(DATABASE)
        db.execute('INSERT INTO users VALUES ("'+email+'","'+name+'","'+imageurl+'","'+token+'");')
    except sqlite3.IntegrityError as e:
        # print("User already in database")
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
        c.execute('INSERT INTO recipe_overview VALUES ("'+filter_bad_input(recipeId)+'","'+filter_bad_input(label.lower())+'","'+filter_bad_input(urllink)+'","2.5");')
        for word in label.split(" "):
            add_recipe_keyword(c, recipeId, word)
    except sqlite3.IntegrityError as e:
        pass
        # print("Recipe already in database")
    except sqlite3.OperationalError as e:
        pass
        # illegal character
    
    db.commit()
    db.close()


# Should NOT be called directly but rather only when new recipes are added through add_recipe_overview_db
def add_recipe_keyword(cursor, recipeId, word):
    cursor.execute('INSERT INTO recipe_keywords VALUES ("'+recipeId+'","'+word.lower()+'");')


# Return entres from recipe_keywords TABLE that have a matching keyword in the recipe_keywords table
def find_recipes_keyword(word):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('SELECT * from recipe_keywords where keyword="'+word.lower()+'";')
    hits = c.fetchall()
    recipes = []
    for hit in hits:
        for recipe in find_recipe_id(c, hit[0]):
            recipes.append(recipe)
    
    db.close()
    return recipes


# Return entries from recipe_overview TABLE that have a matching recipeId 
def find_recipe_id(cursor, recipeId):
    cursor.execute('SELECT * from recipe_overview where recipeID="'+recipeId+'";')
    hits = cursor.fetchall()
    return hits



# Returns upto 'num' amount of random entries from the recipe_overview TABLE
def get_random_recipes(num):
    db = sqlite3.connect(DATABASE)
    c = db.cursor
    c.execute('SELECT * FROM table ORDER BY RANDOM() LIMIT '+num+';')
    db.close()
    return c.fetchall()


# Adds a new entry to the recipe_comment TABLE
def add_recipe_comment(recipeId, comment, username, userimage):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('INSERT INTO recipe_comments VALUES ("'+recipeId+'","'+comment+'","'+username+'","'+userimage+'");')
    db.commit()
    db.close()


# Gets all of the comments for a particular recipeID from the recipe_comment TABLE
def get_recipe_comments(recipeID):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('SELECT * from recipe_comments where recipeID="'+recipeID+'";')
    hits = c.fetchall()
    db.close()
    return hits


def filter_bad_input(data):
    filtered = ''
    for c in data:
        if c not in [",",";","(",")"]:
            filtered += c
    return filtered


init_db()

