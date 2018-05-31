import sys
import sqlite3
import textParser
import ingredientManager
import recipeDataCollector
import costCalculator
import authentication
from sqlite3 import Error


DATABASE = 'recipething.db'
PRODUCT_DB = 'products.db'


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute('CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, fullname TEXT, imageurl TEXT, token TEXT, description TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS user_ratings (userID TEXT, recipeID TEXT, rating INTEGER, FOREIGN KEY (userID) REFERENCES users(userID),FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID))')
    db.execute('CREATE TABLE IF NOT EXISTS user_favourites (userID TEXT, recipeID TEXT, FOREIGN KEY (userID) REFERENCES users(userID), FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID))')
    db.execute('CREATE TABLE IF NOT EXISTS user_shopping_lists (userID TEXT, recipeID TEXT, selectedProducts TEXT, selectedStore TEXT, effectiveCost TEXT, realCost TEXT, FOREIGN KEY (userID) REFERENCES users(userID), FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID))')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_overview (recipeID TEXT PRIMARY KEY NOT NULL, userID INTEGER, recipeLabel TEXT, recipeDescription TEXT, recipeImageLink TEXT, prepTime REAL, recipeInstructions TEXT, recipeClickCount INTEGER, recipeRatingFrequency INTEGER, recipeCumulativeRating INTEGER, recipeCalories INTEGER, recipeDietLabels TEXT, recipeEffectiveCost TEXT, recipeRealCost TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_keywords (recipeID TEXT, keyword TEXT, FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID))')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_ingredients (recipeID TEXT, ingredientDesc TEXT, quantity TEXT, measure TEXT, item TEXT, FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID))')
    db.execute('CREATE TABLE IF NOT EXISTS recipe_comments (recipeID TEXT, userID INTEGER, comment TEXT, FOREIGN KEY (recipeID) REFERENCES recipe_overview(recipeID), FOREIGN KEY (userID) REFERENCES users(userID))')
    db.commit()
    db.close()


# Updates a user in the database or creates a new user if not existent
# This is to update the login token, not to update other fiels
# TODO check the token with Google
def update_user_db(email, name, imageurl, token, description):
    if check_user_db(email) == 0:
        entry = [email, name, imageurl, token, description]
        db = sqlite3.connect(DATABASE)
        db.execute('INSERT INTO users (email, fullname, imageurl, token, description) VALUES (?,?,?,?,?)', entry)
    else:
        # print("User already in database")
        entry = [token, email]
        db = sqlite3.connect(DATABASE)
        db.execute('UPDATE users SET token=? WHERE email=?', entry)
    db.commit()
    db.close()


# Sets the description field for a user in user TABLE for the user with given userID
def set_desc_user_db(userId, desc):
    entry = [desc, userId]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('UPDATE users SET description=? WHERE userID=?', entry)
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


# Checks if a certain user has a certain recipe as favourited by examining user_favourites TABLE
def is_user_favourited_db(userId, recipeId):
    entry = [userId, recipeId]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('SELECT * from user_favourites WHERE userID=? AND recipeID=?', entry)
    hits = c.fetchall()
    if hits == []:
        return False
    return True


# Add a rating to the user_ratings TABLE for a given user and recipe pair
# Also adjusts the rating fields in the recipe_overview TABLE
def add_user_rating_db(userId, recipeId, rating):
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    # If this user has not rated this product
    previousRating = find_user_rating_db(userId, recipeId)
    if previousRating == None:
        entry = [userId, recipeId, rating]
        c.execute('INSERT INTO user_ratings VALUES (?,?,?)', entry)
        entry = [rating, recipeId]
        c.execute('UPDATE recipe_overview SET recipeRatingFrequency=recipeRatingFrequency+1, recipeCumulativeRating=recipeCumulativeRating+? WHERE recipeID=?', entry) 
    # The user has already rated this product
    else:
        entry = [rating, userId, recipeId]
        c.execute('UPDATE user_ratings SET rating=? WHERE userId=? AND recipeId=?', entry)
        entry = [int(rating) - int(previousRating["rating"]), recipeId]
        c.execute('UPDATE recipe_overview SET recipeCumulativeRating=recipeCumulativeRating+? WHERE recipeId=?', entry)
    db.commit()
    db.close()


# Finds the rating that a given user has given a given recipe by examining the user_ratings TABLE
# Clearly returns None if the user has not rated the recipe
def find_user_rating_db(userId, recipeId):
    entry = [userId, recipeId]
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * from user_ratings WHERE userID=? AND recipeID=?', entry)
    hit = c.fetchone()
    db.close()
    return hit


# Returns all entries from recipe_overview TABLE where userdID is userId
# Etc. gets all recipes uploaded by the given user
def find_user_recipes_db(userId):
    entry = [userId]
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * from recipe_overview WHERE userID=?', entry)
    hits = c.fetchall()
    db.close()
    return hits


# Adds a new recipe overview entry and also recipe_keyword entries if we don't have it already
# DietLabels is a list such as ["Balanced", "High-Protein"]
# When a recipe is added for the first time (etc. recieved from edamam or submitted by user, it has it's costs calculated and store so as to not recalculate)
# When a specific recipe page is opened in the future, we recalculate costs due to possibly changed products and edit these values in the recipe_overview TABLE
def add_recipe_overview_db(recipeId, userId, label, urllink, prepTime, parsedInstructions, recipeDesc, recipeCalories, recipeDietLabels):
    tmp = ''
    for item in recipeDietLabels:
        tmp+= item + ","
    recipeDietLabels = tmp[:-1]
    entry = [recipeId, userId, label, recipeDesc, urllink, prepTime, parsedInstructions, recipeCalories, recipeDietLabels]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    try:
        # Starting clickCount is 0. Default ratingFrequency is 1 and cumalativeRating is 4, default best costs 0 until update called
        c.execute('INSERT INTO recipe_overview VALUES (?,?,?,?,?,?,?,0,1,4,?,?,0,0)', entry)
        label = list(set(label.split()))
        for word in label:
            add_recipe_keyword_db(c, recipeId, word)
    except sqlite3.IntegrityError as e:
        # print("Recipe already in database")
        return -1
    except sqlite3.OperationalError as e:
        # illegal character
        return -1

    db.commit()
    db.close()
    return 1


# Should be called whenever a specific recipe page is opened. This will recalculate the costs associated with the recipe due to possible changed products
# Return 0 if the recipe with recipeId doesn't exist in the db
def update_recipe_overview_db(recipeId):
    recipeHit = find_recipe_id_db(recipeId)
    if recipeHit == []:
        return 0

    recipeDict = recipeDataCollector.getRecipeDictionaries([recipeId], [0], authentication.userid, "any", True)[0]
    selectedProducts = []
    for ingredient in recipeDict["ingredients"]:
        selectedProducts.append(0)

    # Calculate the total effective price based on the selectedProducts
    totalEffectiveCost = costCalculator.calcTotalCost(recipeDict, selectedProducts)
    totalRealCost = costCalculator.calcTotalRealCost(recipeDict, selectedProducts)

    entry = ['%0.2f' % totalEffectiveCost, '%0.2f' % totalRealCost, recipeId]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('UPDATE recipe_overview SET recipeEffectiveCost=?, recipeRealCost=? WHERE recipeID=?', entry)
    db.commit()
    db.close()

    return 1

# Increase the recipeClickCount for a recipe in the recipe_overview TABLE
def increment_recipe_clickcount_db(recipeId):
    entry = [recipeId]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    c.execute('UPDATE recipe_overview SET recipeClickCount=recipeClickCount+1 WHERE recipeID=?', entry)
    db.commit()
    db.close()


# Should NOT be called directly but rather only when new recipes are added through add_recipe_overview_db
def add_recipe_keyword_db(cursor, recipeId, word):
    entry = [recipeId, word.lower()]
    cursor.execute('INSERT INTO recipe_keywords VALUES (?,?)', entry)


# Get back n number of random recipe_overview TABLE entries
def get_random_recipes_db(num):
    entry = [num]
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * FROM recipe_overview WHERE recipeID IN (SELECT recipeID FROM recipe_overview ORDER BY RANDOM() LIMIT ?)', entry)
    hits = c.fetchall()
    db.close()
    return hits
    

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


# Returns recipes from recipe_overview TABLE that have matching keywords, exclude matching exclusions and are less than needed preptime
# Does not consider keywords in the recipe Label. User find_recipes_keyword_db for that
def find_recipes_overview_db(included, excluded, prepTime, cost):

    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory 
    c = db.cursor()      

    # Note because of the way this function is called, only one 'included' term is given at a time. etc. only "milk"
    # Get all hits that has an INCLUDED as a substring of the item text field
    c.execute('SELECT * from recipe_ingredients WHERE item LIKE ?', [str("%"+str(included)+"%")])
    recipeIDHits = c.fetchall()
    
    resultRecipeIDs = []
    for recipeID in recipeIDHits:
        resultRecipeIDs.append(recipeID["recipeID"])

    # Get the recipe_overview entries for each recipe with the included ingredient
    excludedRecipeIDs = []
    excluded = textParser.filterInput(excluded)
    excluded = excluded.split()
    for exclude in excluded:
        c.execute('SELECT * from recipe_ingredients WHERE item LIKE ?', [str("%"+str(exclude)+"%")])
        excludedHits = c.fetchall()
        for item in excludedHits:
            excludedRecipeIDs.append(item["recipeID"])        

    # Remove all excludedRecipeIDs from the resultRecipeIDs
    for excludedID in excludedRecipeIDs:
        try:
            resultRecipeIDs.remove(excludedID)
        except ValueError:
            pass

    # Remove all the are too timely
    finalRecipes = []
    for recipeID in resultRecipeIDs:
        c.execute('SELECT * from recipe_overview WHERE recipeID=? AND prepTime<=?', [recipeID, prepTime])
        result = c.fetchone()
        if result != None:
            finalRecipes.append(result)

    # Save demo time
    finalRecipes = finalRecipes[:9]

    # Try to get 9 recipes that are cheap enough
    finalfinalRecipes = []
    for recipe in finalRecipes:
        print("CHECK")
        print(recipe["recipeID"])
        if recipeDataCollector.getRecipeDictionaries([recipe["recipeID"]], [0], authentication.userid, "any", False)[0]["effectiveCost"] < cost:
            finalfinalRecipes.append(recipe)

    return finalfinalRecipes


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
# If shopname is not None then only look for products in that shop
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
def get_product_overview_db(productId, shopname):
    db = sqlite3.connect(PRODUCT_DB)
    db.row_factory = dict_factory
    c = db.cursor()
    hit = []
    if shopname == None:
        entry = [productId]
        c.execute('SELECT * from product_overview WHERE productID=?', entry)
        hit = c.fetchone()
    else:
        entry = [productId, shopname]
        c.execute('SELECT * from product_overview WHERE productID=? AND store=?', entry)
        hit = c.fetchone()
    db.close()
    return hit



# Saves a users choice of products for a given recipe. 
# selectedProducts is the selectedProduct[] list in recipe route
def update_user_shopping_list(userId, recipeId, selectedProducts, selectedStore, effectiveCost, realCost):
    tmp = ''
    for productIndex in selectedProducts:
        tmp += str(productIndex) + ','
    selectedProducts = tmp[:-1]
    entry = [userId, recipeId, selectedProducts, selectedStore, effectiveCost, realCost]
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    # If the user doesnt have a shopping list for this recipe
    if get_user_shopping_list(userId, recipeId) == None:
        c.execute('INSERT INTO user_shopping_lists VALUES (?,?,?,?,?,?)', entry)
    else:
        entry = [selectedProducts, selectedStore, effectiveCost, realCost, userId, recipeId]
        c.execute('UPDATE user_shopping_lists SET selectedProducts=?, selectedStore=?, effectiveCost=?, realCost=? WHERE userId=? AND recipeId=?', entry)
    db.commit()
    db.close()


# Get the entry from the user_shopping_list TABLE for a given userId and recipeId pair
def get_user_shopping_list(userId, recipeId):
    entry = [userId, recipeId]
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * from user_shopping_lists WHERE userID=? AND recipeID=?', entry)
    hit = c.fetchone()
    db.close()
    return hit


# Gets all the shopping lists for a given user from the user_shopping_list TABLE
def get_user_shopping_lists(userId):
    entry = [userId]
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute('SELECT * from user_shopping_lists WHERE userID=?', entry)
    hits = c.fetchall()
    db.close()
    return hits    


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
