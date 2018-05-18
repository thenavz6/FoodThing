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
from helperFunctions import *


@app.route("/",methods=["GET", "POST"])
def main():
    return render_template("login.html")


@app.route("/error",methods=["GET", "POST"])
def error():
    return render_template("error.html")


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
@app.route("/dashboard",methods=["GET", "POST"])
def dashboard():
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    # If the 'random' search term is in the recipe name it is ideal since then dashboard items can be stored and picked from our database.
    return searchRecipe("food")


# Does essentially the same as the above. Except based on search query text - so the above should populate with random recipes.
@app.route("/searchRecipe/<query>", methods=["GET", "POST"])
def searchRecipe(query):
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    # Initialise required values
    global recipeId
    recipeLabels, recipeImageLinks, recipeIngredients = [], [], []
    rand = random.randint(1,50)

    if request.method == "GET":
        recipeId = []
        # With a recipe search, we get at most half (5) of the items from our database if possible
        # Won't handle multi worded queries very well. Dealing with multi worded queries is a whole different problem too.
        # This is to reduce API calls
        databaseRecipes = database.find_recipes_keyword_db(query)
        for num in randomSortedNumbers(len(databaseRecipes)):
            if len(recipeId) >= 5:
                break
            recipeId.append(databaseRecipes[num]["recipeID"])
            recipeLabels.append(databaseRecipes[num]["recipeLabel"])
            recipeImageLinks.append(databaseRecipes[num]["recipeImageLink"])

        # Fill in the remaining slots with API Calls (new recipes not in our database)
        remainder = 9 - len(recipeId)
        response = requests.get("https://api.edamam.com/search?q="+str(query)+"&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca&from="+str(rand)+"&to="+str(rand+remainder))
        if (response.status_code != 200):
            return redirect(url_for("error"))
        jsonData = response.json()["hits"]

        # For each item/recipe we get back we will append them onto our lists
        for item in jsonData:
            recipeId.append(item.get('recipe').get('uri').split("_",1)[1])
            recipeLabels.append(item.get('recipe').get('label'))
            recipeImageLinks.append(item.get('recipe').get('image'))
            recipeIngredients = []
            for ingredient in item.get('recipe').get('ingredients'):
                recipeIngredients.append(ingredient.get('text'))

            # Add the recipe and its properties to the database too for faster future searches if we don't have a record of it already
            if database.add_recipe_overview_db(item.get('recipe').get('uri').split("_",1)[1], -1, item.get('recipe').get('label'), item.get('recipe').get('image'),item.get('recipe').get('totalTime')) != -1:
                database.add_recipe_ingredients_db(item.get('recipe').get('uri').split("_",1)[1], recipeIngredients)

    # Possible post requests
    if request.method == "POST":
        if request.form["bt"] == 'logout':
            authentication.is_authenticated = False;
            return redirect(url_for("main"))
        if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
            return redirect(url_for("searchRecipe", query = request.form["searchtext"]))
        if request.form["bt"][:6] == "recipe":
            return redirect(url_for("recipe", recipeId = recipeId[int(request.form["bt"][7:])]))

    return render_template("dashboard.html", labelList = recipeLabels, imageList = recipeImageLinks, userid = authentication.userid, imageurl = authentication.imageurl)


@app.route("/advancedSearchPage", methods=["GET", "POST"])
def advancedSearchPage():
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    if request.method == "GET":
        return render_template("advancedSearch.html")
    if request.method == "POST":
        if request.form["bt"] == 'logout':
            authentication.is_authenticated = False;
            return redirect(url_for("main"))
        if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
            return redirect(url_for("searchRecipe", query = request.form["searchtext"]))
        if request.form["bt"] == "AdvancedSearch":
            print(request.form["KeyWords"])
            print(request.form["excludedIngredients"])
            print(request.form["maxPrepTime"])
            return redirect(url_for("advancedSearch",included = request.form["KeyWords"], excluded = request.form["excludedIngredients"],prepTime = request.form["maxPrepTime"]))



@app.route("/advancedSearch/<included>/<excluded>/<prepTime>", methods=["GET", "POST"])
def advancedSearch(included,excluded,prepTime):
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    # Initialise required values
    global recipeId
    recipeLabels, recipeImageLinks, recipeIngredients = [], [], []
    rand = random.randint(1,50)

    if request.method == "GET":
        recipeId = []
        # With a recipe search, we get at most half (5) of the items from our database if possible
        # Won't handle multi worded queries very well. Dealing with multi worded queries is a whole different problem too.
        # This is to reduce API calls
        print(included)
        print(excluded)
        print(prepTime)
        databaseRecipes = database.find_recipes_overview_db(included, excluded, prepTime)
        for num in randomSortedNumbers(len(databaseRecipes)):
            if len(recipeId) >= 5:
                break
            recipeId.append(databaseRecipes[num]["recipeID"])
            recipeLabels.append(databaseRecipes[num]["recipeLabel"])
            recipeImageLinks.append(databaseRecipes[num]["recipeImageLink"])

        # Fill in the remaining slots with API Calls (new recipes not in our database)
        remainder = 9 - len(recipeId)
        exclusionQuery = "+".join(excluded.split(","))
        inclusionQuery = included
        response = requests.get("https://api.edamam.com/search?q="+str(inclusionQuery)+"&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca&from="+str(rand)+"&to="+str(rand+remainder)+"&excluded="+exclusionQuery+"&time="+prepTime)
        if (response.status_code != 200):
            return redirect(url_for("error"))
        jsonData = response.json()["hits"]

        # For each item/recipe we get back we will append them onto our lists
        for item in jsonData:
            recipeId.append(item.get('recipe').get('uri').split("_",1)[1])
            recipeLabels.append(item.get('recipe').get('label'))
            recipeImageLinks.append(item.get('recipe').get('image'))
            recipeIngredients = []
            for ingredient in item.get('recipe').get('ingredients'):
                recipeIngredients.append(ingredient.get('text'))

            # Add the recipe and its properties to the database too for faster future searches if we don't have a record of it already
            if database.add_recipe_overview_db(item.get('recipe').get('uri').split("_",1)[1], -1, item.get('recipe').get('label'), item.get('recipe').get('image'),item.get('recipe').get('totalTime')) != -1:
                database.add_recipe_ingredients_db(item.get('recipe').get('uri').split("_",1)[1], recipeIngredients)

    # Possible post requests
    if request.method == "POST":
        if request.form["bt"] == 'logout':
            authentication.is_authenticated = False;
            return redirect(url_for("main"))
        if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
            return redirect(url_for("searchRecipe", query = request.form["searchtext"]))
        if request.form["bt"][:6] == "recipe":
            return redirect(url_for("recipe", recipeId = recipeId[int(request.form["bt"][7:])]))

    return render_template("dashboard.html", labelList = recipeLabels, imageList = recipeImageLinks, userid = authentication.userid, imageurl = authentication.imageurl)

# The 'specific' recipe page that details instructions and ingredients.
# Later this should lead to the substitution pop-up box and so and so.
@app.route("/recipe/<recipeId>", methods=["GET", "POST"])
def recipe(recipeId):
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    # Initialise these values
    recipeLabel, recipeImage, recipeIngredients, ingredientProducts = "", "", [], []

    # First check if we have this recipe in our database already which will be true if it appeared in a search query
    # Makes future requests (like favouriting and commenting MUCH FASTER)
    recipeHit = database.find_recipe_id_db(recipeId)
    if recipeHit != None:
        recipeLabel = recipeHit["recipeLabel"]
        recipeImage = recipeHit["recipeImageLink"]
        for ingredient in database.find_recipe_ingredients_db(recipeId):
            recipeIngredients.append(ingredient["ingredientDesc"])

    # Only if we do not have it in the db then we ask edamam
    else:
        response = requests.get("https://api.edamam.com/search?r=\
    http%3A%2F%2Fwww.edamam.com%2Fontologies%2Fedamam.owl%23recipe_"+str(recipeId)+"&app_id=c565299e&app_key=\
    b90e6fb2878260b8f991bd4f9a8663ca")

        if (response.status_code != 200):
            return redirect(url_for("error"))
        try:
            recipe = response.json()[0]
        except IndexError:
            return redirect(url_for("error"))
        recipeLabel = recipe.get('label')
        recipeImage = recipe.get('image')
        prepTime = recipe.get('totalTime')
        for ingredient in recipe.get('ingredients'):
            recipeIngredients.append(ingredient.get('text'))
        # Also add the recipe to the db since we didn't have it
        database.add_recipe_overview_db(recipeId, -1, recipeLabel, recipeImage,prepTime)
        database.add_recipe_ingredients_db(recipeId, recipeIngredients)

    # Check if the user has favourited this recipe
    isFavourited = False
    userFavourites = database.find_user_favourites_db(authentication.userid)
    for favourite in userFavourites:
        if recipeId == favourite["recipeID"]:
            isFavourited = True

    # Retrieve all comments and the users who left those comments
    usersWhoCommented = []
    recipeComments = []
    for entry in database.get_recipe_comments_db(recipeId):
        recipeComments.append(entry["comment"])
        usersWhoCommented.append(database.find_user_by_id_db(int(entry["userID"])))

    # Find all relevent product hits for each ingredient
    for ingredient in database.find_recipe_ingredients_db(recipeId):
        ingredientProducts.append(productFinder.findBestProducts(ingredient))

    costCalculator.calcBestCost(ingredientProducts)

    # Possible post requests
    if request.method == "POST":
        print(request.form.get("0"))
        if "bt" in request.form:
            if request.form["bt"] == 'logout':
                authentication.is_authenticated = False;
                return redirect(url_for("main"))
            if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
                return redirect(url_for("searchRecipe", query = request.form["searchtext"]))
            if request.form["bt"] == "comment":
                database.add_recipe_comment_db(recipeId, authentication.userid, request.form["commentText"])
                return redirect(url_for("recipe", recipeId = recipeId))
            if request.form["bt"] == "Favourite":
                database.add_user_favourite_db(authentication.userid, recipeId)
                return redirect(url_for("recipe", recipeId = recipeId))
            if request.form["bt"] == "Unfavourite":
                database.delete_user_favourite_db(authentication.userid, recipeId)
                return redirect(url_for("recipe", recipeId = recipeId))
        if "user" in request.form:
            return redirect(url_for("userprofile", userId = int(request.form["user"])))

    return render_template("recipe.html", recipeId = recipeId, recipeLabel = recipeLabel, recipeImage = recipeImage, recipeIngredients = recipeIngredients, ingredientProducts = ingredientProducts, userid = authentication.userid, imageurl = authentication.imageurl, isFavourited = isFavourited, recipeComments = recipeComments, usersWhoCommented = usersWhoCommented)


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
        if request.form["bt"] == 'logout':
            authentication.is_authenticated = False;
            return redirect(url_for("main"))
        if request.form["bt"] == "Upload Recipe":
            return redirect(url_for("uploadRecipe"))
        if request.form["bt"] == "UpdateDesc":
            database.set_desc_user_db(authentication.userid, request.form["updatedesc"])
            return redirect(url_for("userprofile", userId = userId))
        if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
            return redirect(url_for("searchRecipe", query = request.form["searchtext"]))

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
        if "add_ingred_bt" in request.form:
            savedLabel = request.form["recipename"]
            savedImageurl = request.form["imageurl"]
            if request.form["ingredient_"+str(numOfIngredients-1)].strip() != '':
                savedIngredients.append(request.form["ingredient_"+str(numOfIngredients-1)])
                numOfIngredients += 1
        if "add_step_bt" in request.form:
            savedLabel = request.form["recipename"]
            savedImageurl = request.form["imageurl"]
            if request.form["step_"+str(numOfSteps-1)].strip() != '':
                savedSteps.append(request.form["step_"+str(numOfSteps-1)])
                numOfSteps += 1
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
