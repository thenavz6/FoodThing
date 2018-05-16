# Code adapted from http://flask.pocoo.org/docs/0.12/patterns/sqlite3/

import sqlite3
from flask import *
import ingredientManager

app = Flask(__name__)

DATABASE = 'database.db'
PRODUCT_DB = 'products.db'

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute('CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, fullname TEXT, imageurl TEXT, token TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS user_favourites (userID TEXT, recipeID TEXT, FOREIGN KEY (userID) REFERENCES users(userID), FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID))')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_overview (recipeID TEXT PRIMARY KEY NOT NULL, userID INTEGER, recipeLabel TEXT, recipeImageLink TEXT, recipeRating REAL)')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_keywords (recipeID TEXT, keyword TEXT, FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID))')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_ingredients (recipeID TEXT, ingredientDesc TEXT, quantity TEXT, measure TEXT, item TEXT, FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID))')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_comments (recipeID TEXT, userID INTEGER, comment TEXT, FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID), FOREIGN KEY (userID) REFERENCES users(userID))')
    db.commit()
    db.close()


# Updates a user in the database or creates a new user if not existent
# TODO check the token with Google
def update_user_db(email, name, imageurl, token):
    if check_user_db(email) == 0:
        entry = [email, name, imageurl, token]
        db = sqlite3.connect(DATABASE)        
        db.execute('INSERT INTO users (email, fullname, imageurl, token) VALUES (?,?,?,?)', entry)
    else:
        # print("User already in database")
        entry = [token, email]
        db = sqlite3.connect(DATABASE)
        db.execute('UPDATE users SET token=? WHERE email=?', entry)
    db.commit()
    db.close()


# Returns 1 if this a user with the given email already exists in the users TABLE
def check_user_db(email):
    entry = [email]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('SELECT * from users WHERE email=?', entry)
    a = c.fetchall()
    db.close()
    return len(a)


# Return the entry row for a user with given userID from the user TABLE
def find_user_by_id_db(userId):
    entry = [userId]
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * from users WHERE userID=?', entry)
    hit = c.fetchone()
    db.close()
    return hit


# Return the entry row for a user with given email from the user TABLE
def find_user_by_email_db(email):
    entry = [email]
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * from users WHERE email=?', entry)
    hit = c.fetchone()
    db.close()
    return hit


# Returns 1 if the current token associated to this email matches the argument token
def compare_token_db(email, token):
    entry = [email]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('SELECT * from users WHERE email=?', entry)
    a = c.fetchone()
    db.close()
    if a == None or a[3] != token:
        return 0
    return 1


# Adds a new entry to represent favourite recipe by user into user_favourites TABLE
def add_user_favourite_db(userId, recipeId):
    entry = [userId, recipeId]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('INSERT INTO user_favourites VALUES (?,?)', entry)
    db.commit()
    db.close()


# Deletes an existing entry of favourite recipe from the user_favourites TABLE
def delete_user_favourite_db(userId, recipeId):
    entry = [userId, recipeId]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('DELETE FROM user_favourites WHERE userID=? AND recipeID=?', entry)
    db.commit()
    db.close()


# Returns all entries for users favourite recipes from user_favourites TABLE
def find_user_favourites_db(userId):
    entry = [userId]
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * from user_favourites WHERE userID=?', entry)
    hits = c.fetchall()
    db.close()
    return hits


# Adds a new recipe overview entry and also recipe_keyword entries
def add_recipe_overview_db(recipeId, userId, label, urllink):
    entry = [recipeId, userId, label, urllink]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    try:
        c.execute('INSERT INTO recipe_overview VALUES (?,?,?,?,"2.5")', entry)
        for word in label.split(" "):
            add_recipe_keyword_db(c, recipeId, word)
    except sqlite3.IntegrityError as e:
        # print("Recipe already in database")
        return -1
    except sqlite3.OperationalError as e:
        pass
        # illegal character

    db.commit()
    db.close()
    return 1


# Should NOT be called directly but rather only when new recipes are added through add_recipe_overview_db
def add_recipe_keyword_db(cursor, recipeId, word):
    entry = [recipeId, word.lower()]
    cursor.execute('INSERT INTO recipe_keywords VALUES (?,?)', entry)


# Return entres from recipe_keywords TABLE that have a matching keyword in the recipe_keywords table
def find_recipes_keyword_db(word):
    entry = [word.lower()]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('SELECT * from recipe_keywords WHERE keyword=?', entry)
    hits = c.fetchall()
    recipes = []
    for hit in hits:
        recipe = find_recipe_id_db(hit[0])
        recipes.append(recipe)
    db.close()
    return recipes


# Return entries from recipe_overview TABLE that have a matching recipeId
def find_recipe_id_db(recipeId):
    entry = [recipeId]
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    cursor = db.cursor()
    cursor.execute('SELECT * from recipe_overview WHERE recipeID=?', entry)
    hits = cursor.fetchone()
    db.close()
    return hits


# Creates entries in the recipe_ingredients TABLE for each ingredient associated with this recipe
# Uses the IngredientManager to extract important information from user supplied ingredient String
# Components of an ingredient are: amount, unitofmeasure, text
def add_recipe_ingredients_db(recipeId, ingredientList):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    for ingredient in ingredientList:
        components = ingredientManager.convertIngredient(ingredient)
        entry = [recipeId, ingredient.lower(), components[0], components[1], components[2]]
        c.execute('INSERT INTO recipe_ingredients VALUES (?,?,?,?,?)', entry)
    db.commit()
    db.close()


# Returns all entries of ingredients for the given recipeId from recipe_ingredients TABLE
def find_recipe_ingredients_db(recipeId):
    entry = [recipeId]
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * from recipe_ingredients WHERE recipeID=?', entry)
    hits = c.fetchall()
    db.close()
    return hits


# Adds a new entry to the recipe_comment TABLE
def add_recipe_comment_db(recipeId, userId, comment):
    entry = [recipeId, userId, filter_bad_input(comment)]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('INSERT INTO recipe_comments VALUES (?,?,?)', entry)
    db.commit()
    db.close()


# Gets all of the comments for a particular recipeID from the recipe_comment TABLE
def get_recipe_comments_db(recipeId):
    entry = [recipeId]
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * from recipe_comments WHERE recipeID=?', entry)
    hits = c.fetchall()
    db.close()
    return hits


# Gets all of the products from the product_keywords TABLE that have a matching keyword
def find_products_keyword_db(word):
    entry = [word]
    db = sqlite3.connect(PRODUCT_DB)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * from product_keywords WHERE keyword=?', entry)
    hits = c.fetchall()
    db.close()
    return hits


# Find the product from the product_overview TABLE that has the matching productId
def get_product_overview_db(productId):
    entry = [productId]
    db = sqlite3.connect(PRODUCT_DB)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * from product_overview WHERE productID=?', entry)
    hit = c.fetchone()
    db.close()
    return hit


# General parsing out of possible injection / malicious characters
def filter_bad_input(data):
    filtered = ''
    for c in data:
        if c not in ["'",";","=",'"']:
            filtered += c
    return filtered


# Let's us reference return entries by column name as well as index
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


init_db()

