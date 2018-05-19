from flask import *
import requests
import json

import authentication
import server
from server import app
import database
import textParser
import productFinder
import costCalculator
import recipeDataCollector
from helperFunctions import *

# Some global settings
OFFLINEMODE = False                              # Will not contact edamam for search queries. Only source locally.

@app.route("/",methods=["GET", "POST"])
def main():
    return render_template("login.html")


@app.route("/error",methods=["GET", "POST"])
def error():
    return render_template("error.html")


# Since the header and it's functionality is common for post pages, it is better to place its code
# in one common area. Pass the request.form as the argument
def headerRequests(requestform):
    if "headerbt" in requestform:
        if requestform["headerbt"] == "Logout":
            authentication.is_authenticated = False
            return redirect(url_for("main"))
        if requestform["headerbt"] == "Search" and requestform["searchtext"].strip() != "":
            return redirect(url_for("searchRecipe", query = requestform["searchtext"]))
        if requestform["headerbt"] == "Add Recipe":
            return redirect(url_for("uploadRecipe"))
        if requestform["headerbt"] == "Profile":
            return redirect(url_for("userprofile", userId = authentication.userid))
    return None


# The possible requests that can be made from a 'Recipe Card' (just favouriting atm, add star rating later)
def recipeCardRequests(requestform):
    print(requestform)
    if "Favourite" in requestform:
        database.add_user_favourite_db(authentication.userid, requestform["Favourite"])
        return True
    if "Unfavourite" in requestform:
        database.delete_user_favourite_db(authentication.userid, requestform["Unfavourite"])
        return True
    return None

# We need to verify this token with Google for security. So TODO that later.
# After verification, we create a database account for the user and update their token.
@app.route("/updateToken", methods=["GET", "POST"])
def updateToken():
    database.update_user_db(request.form['email'], request.form['fullname'], request.form['imageurl'], request.form['token'], "This is my profile!")
    user = database.find_user_by_email_db(request.form['email'])

    # print(authentication.xor(request.form['token']))
    if (user == None):
        return -1

    authentication.is_authenticated = True
    authentication.userid = int(user["userID"])
    authentication.email = request.form['email']
    authentication.username = request.form['fullname']
    authentication.imageurl = request.form['imageurl']
    authentication.current_token = request.form['token']
    return "Success"


# Had to make this ugly global variable to retain the same recipeId list in between the GET and POST
# Otherwise when the user clicked on a recipe, we were making the API requests again and this took the user to the wrong recipe.
recipeId = []
recipes = []
@app.route("/dashboard",methods=["GET", "POST"])
def dashboard():
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    # If the 'random' search term is in the recipe name it is ideal since then dashboard items can be stored and picked from our database.
    return searchRecipe(getRandomSearch())


# Does essentially the same as the above. Except based on search query text - so the above should populate with random recipes.
@app.route("/searchRecipe/<query>", methods=["GET", "POST"])
def searchRecipe(query):
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    return advancedSearch(query, None, None)


@app.route("/advancedSearchPage", methods=["GET", "POST"])
def advancedSearchPage():
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    if request.method == "GET":
        return render_template("advancedSearch.html")
    if request.method == "POST":
        if headerRequests(request.form) != None:
            return headerRequests(request.form) 
        if "bt" in request.form and request.form["bt"] == "AdvancedSearch":
            print(request.form["KeyWords"])
            print(request.form["excludedIngredients"])
            print(request.form["maxPrepTime"])
            return redirect(url_for("advancedSearch", query = request.form["KeyWords"], excluded = request.form["excludedIngredients"], prepTime = request.form["maxPrepTime"]))


@app.route("/advancedSearch/<query>/<excluded>/<prepTime>", methods=["GET", "POST"])
def advancedSearch(query,excluded,prepTime):
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    global recipeId
    global recipes    

    if request.method == "GET":
        if OFFLINEMODE == False:
            # Everytime a search is done, we will ask edamam for 5 recipes that we also add locally
            recipeDataCollector.receiveRecipeData(query, 5, excluded, prepTime)
        
        # Look through our database to get all recipeIds for hit recipes. Caps at 9 results.
        recipeId, databaseRecipes = [], []
        if excluded == None:
            databaseRecipes = database.find_recipes_keyword_db(query)
        else:
            databaseRecipes = database.find_recipes_overview_db(query, excluded, prepTime)
        for num in randomSortedNumbers(len(databaseRecipes)):
            if len(recipeId) >= 9:
                break
            recipeId.append(databaseRecipes[num]["recipeID"])

        recipes = recipeDataCollector.getRecipeDictionaries(recipeId, authentication.userid)

    # Possible post requests
    if request.method == "POST":
        if headerRequests(request.form) != None:
            return headerRequests(request.form)    
        if recipeCardRequests(request.form) != None:
            return redirect(url_for("userprofile", userId = authentication.userid))
        if "advbt" in request.form:
            return redirect(url_for("advancedSearchPage"))
        if "sortbt" in request.form:
            recipes = recipeDataCollector.sortRecipeDictionaries(recipes, request.form["sorttype"])
        if "bt" in request.form and request.form["bt"][:9] == "recipehit":
            return redirect(url_for("recipe", recipeId = request.form["bt"][10:]))

    return render_template("dashboard.html", recipes = recipes, userid = authentication.userid, imageurl = authentication.imageurl)


# The 'specific' recipe page that details instructions and ingredients.
# Later this should lead to the substitution pop-up box and so and so.
recipeDict = {}
@app.route("/recipe/<recipeId>", methods=["GET", "POST"])
def recipe(recipeId):
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    global recipeDict

    # First check if we have this recipe in our database already which will be true if it appeared in a search query
    # Makes future requests (like favouriting and commenting MUCH FASTER)
    recipeHit = database.find_recipe_id_db(recipeId)
    if recipeHit == []:
        recipeDataCollector.recieveSingleRecipe(recipeId)
        recipeHit = database.find_recipe_id_db(recipeId)

    if request.method == "GET":
        recipeDict = recipeDataCollector.getRecipeDictionaries([recipeId], authentication.userid)[0]

    # Retrieve all comments and the users who left those comments
    usersWhoCommented = []
    recipeComments = []
    for entry in database.get_recipe_comments_db(recipeId):
        recipeComments.append(entry["comment"])
        usersWhoCommented.append(database.find_user_by_id_db(int(entry["userID"])))

    # Possible post requests
    if request.method == "POST":
        if headerRequests(request.form) != None:
            return headerRequests(request.form)    
        if recipeCardRequests(request.form) != None:
            return redirect(url_for("recipe", recipeId = recipeId))
        if "bt" in request.form:
            if request.form["bt"] == "comment":
                database.add_recipe_comment_db(recipeId, authentication.userid, request.form["commentText"])
                return redirect(url_for("recipe", recipeId = recipeId))
        if "user" in request.form:
            return redirect(url_for("userprofile", userId = int(request.form["user"])))

    return render_template("recipe.html", recipeDict = recipeDict, userid = authentication.userid, imageurl = authentication.imageurl, recipeComments = recipeComments, usersWhoCommented = usersWhoCommented)


# The page for viewing any user's profile
@app.route("/user/<userId>", methods=["GET", "POST"])
def userprofile(userId):
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    # Default name and image passed if user not found
    profilename = "No one lives here :("
    profileimage = "https://i.vimeocdn.com/portrait/1274237_300x300"
    profilefavourites = []
    profilerecipes = []

    # Find the given user in the database or error for non-integer input
    try:
        userHit = database.find_user_by_id_db(int(userId))
    except ValueError as e:
        return redirect(url_for("error"))

    # Load parameters based on database result
    if userHit != None:
        profilename = userHit["fullname"]
        profileimage = userHit["imageurl"]
        profilefavourites = []

        findfavourites = database.find_user_favourites_db(userId)
        tmp = []
        for favourite in findfavourites:
            tmp.append(favourite["recipeID"])
        for favourite in tmp:
            profilefavourites.append(database.find_recipe_id_db(favourite))

        findRecipes = database.find_user_recipes_db(userId)
        for recipe in findRecipes:
            profilerecipes.append(recipe)

    # Possible post requests
    if request.method == "POST":
        if headerRequests(request.form) != None:
            return headerRequests(request.form) 
        if "bt" in request.form:   
            if request.form["bt"] == "Upload Recipe":
                return redirect(url_for("uploadRecipe"))
            if request.form["bt"] == "UpdateDesc":
                database.set_desc_user_db(authentication.userid, request.form["updatedesc"])
                return redirect(url_for("userprofile", userId = userId))

    return render_template("userprofile.html", profileid = userId, profileuser = userHit, profilerecipes = profilerecipes, profilefavourites = profilefavourites, myuserid = authentication.userid, userimage = authentication.imageurl)


savedLabel = ''
savedImageurl = ''
numOfIngredients = 1
savedIngredients = []
numOfSteps = 1
savedSteps = []
# The page for uploading user recipes
@app.route("/uploadRecipe", methods=["GET", "POST"])
def uploadRecipe():
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    global numOfIngredients
    global numOfSteps
    global savedIngredients
    global savedSteps
    global savedLabel
    global savedImageurl

    # Reset the number of ingredients and steps for this page
    if request.method == "GET":
        numOfIngredients = 1
        numOfSteps = 1
        savedIngredients = []
        savedSteps = []

    if request.method == "POST":
        if headerRequests(request.form) != None:
            return headerRequests(request.form) 
        # Adds an ingredient text field to the form
        if "add_ingred_bt" in request.form:
            savedLabel = request.form["recipename"]
            savedImageurl = request.form["imageurl"]
            if request.form["ingredient_"+str(numOfIngredients-1)].strip() != '':
                savedIngredients.append(request.form["ingredient_"+str(numOfIngredients-1)])
                numOfIngredients += 1
        # Adds a step text field to the form
        if "add_step_bt" in request.form:
            savedLabel = request.form["recipename"]
            savedImageurl = request.form["imageurl"]
            if request.form["step_"+str(numOfSteps-1)].strip() != '':
                savedSteps.append(request.form["step_"+str(numOfSteps-1)])
                numOfSteps += 1
        # Submit the recipe to our database using the form fields
        if "submit_bt" in request.form:
            # Hope this doesn't hit already existed id when appended with userid
            rand = random.randint(1,10000)
            recipeId = str(authentication.userid) + "recipe" + str(rand)
            database.add_recipe_overview_db(recipeId, authentication.userid, request.form["recipename"], request.form["imageurl"], 0)
            ingredientList = []
            for i in range(numOfIngredients):
                ingredientList.append(textParser.seperateAlphaAndDigit(request.form["ingredient_"+str(i)]))
            database.add_recipe_ingredients_db(recipeId, ingredientList)
            for i in range(numOfSteps):
                pass
                # print(request.form["step_"+str(i)])
            return redirect(url_for("recipe", recipeId = recipeId))

    return render_template("uploadrecipe.html", numOfIngredients = numOfIngredients, numOfSteps = numOfSteps, savedIngredients = savedIngredients, savedSteps = savedSteps, savedLabel = savedLabel, savedImageurl = savedImageurl, userid = authentication.userid, userimage = authentication.imageurl)
