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
OFFLINEMODE = True                              # Will not contact edamam for search queries. Only source locally.

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
sortType = "Cost"
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

    global recipeId, recipes, sortType

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

        recipes = recipeDataCollector.getRecipeDictionaries(recipeId, authentication.userid, None)

    # Possible post requests
    if request.method == "POST":
        if headerRequests(request.form) != None:
            return headerRequests(request.form)
        if recipeCardRequests(request.form) != None:
            return redirect(url_for("userprofile", userId = authentication.userid))
        if "advbt" in request.form:
            return redirect(url_for("advancedSearchPage"))
        if "sortbt" in request.form:
            sortType = request.form["sorttype"]
            recipes = recipeDataCollector.sortRecipeDictionaries(recipes, sortType)
        if "bt" in request.form and request.form["bt"][:9] == "recipehit":
            return redirect(url_for("recipe", recipeId = request.form["bt"][10:]))

    return render_template("dashboard.html", recipes = recipes, sortType = sortType, userid = authentication.userid, imageurl = authentication.imageurl)


# The 'specific' recipe page that details instructions and ingredients.
# Later this should lead to the substitution pop-up box and so and so.
recipeDict = {}
selectedProducts = []
prefStore = "any"
@app.route("/recipe/<recipeId>", methods=["GET", "POST"])
def recipe(recipeId):
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    global recipeDict, selectedProducts, prefStore

    # First check if we have this recipe in our database already which will be true if it appeared in a search query
    # Makes future requests (like favouriting and commenting MUCH FASTER)
    recipeHit = database.find_recipe_id_db(recipeId)
    if recipeHit == []:
        recipeDataCollector.recieveSingleRecipe(recipeId)
        recipeHit = database.find_recipe_id_db(recipeId)

    if request.method == "GET":
        recipeDict = recipeDataCollector.getRecipeDictionaries([recipeId], authentication.userid, prefStore)[0]
        # By default we select the cheapest, most relevent products
        selectedProducts = []
        for ingredient in recipeDict["ingredients"]:
            selectedProducts.append(0)

    # Calculate the total effective price based on the selectedProducts
    totalEffectiveCost, i = 0, 0
    for ingredient in recipeDict["ingredients"]:
        try:
            totalEffectiveCost += recipeDict["ingredientProducts"][i][selectedProducts[i]]["effectiveCost"]
        except IndexError:
            pass
        i += 1


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
        if "storebt" in request.form:
            prefStore = request.form["selectstore"]
            recipeDict = recipeDataCollector.getRecipeDictionaries([recipeId], authentication.userid, prefStore)[0]
            # Reset product preferences
            for i in range(0, len(selectedProducts)):
                selectedProducts[i] = 0
            # Recalculate the total effective price based on the selectedProducts
            totalEffectiveCost, i = 0, 0
            for ingredient in recipeDict["ingredients"]:
                try:
                    totalEffectiveCost += recipeDict["ingredientProducts"][i][selectedProducts[i]]["effectiveCost"]
                except IndexError:
                    pass
                i += 1
        if "productbt" in request.form:
            selectedProducts[int(request.form["productbt"].split("_")[0])] = int(request.form["productbt"].split("_")[1])
            # Recalculate the total effective price based on the selectedProducts
            totalEffectiveCost, i = 0, 0
            for ingredient in recipeDict["ingredients"]:
                try:
                    totalEffectiveCost += recipeDict["ingredientProducts"][i][selectedProducts[i]]["effectiveCost"]
                except IndexError:
                    pass
                i += 1

    return render_template("recipe.html", recipeDict = recipeDict, prefStore = prefStore, selectedProducts = selectedProducts, totalEffectiveCost = "%0.2f" % totalEffectiveCost, steps = recipeDict["instructions"].split(";")[:-1], userid = authentication.userid, imageurl = authentication.imageurl, recipeComments = recipeComments, usersWhoCommented = usersWhoCommented)


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
        profilefavourites = recipeDataCollector.getRecipeDictionaries(tmp, authentication.userid, None)


        findRecipes = database.find_user_recipes_db(userId) 
        tmp = []
        for recipe in findRecipes:
            tmp.append(recipe["recipeID"])
        profilerecipes = recipeDataCollector.getRecipeDictionaries(tmp, authentication.userid, None)
                
    profileuser = {
        "id"   : userId,
        "name" : profilename,
        "image": profileimage
    }

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

    return render_template("userprofile.html", profileuser = profileuser, profilerecipes = profilerecipes, profilefavourites = profilefavourites, myuserid = authentication.userid, userimage = authentication.imageurl)


savedLabel = ''
savedImageurl = ''
savedPreptime = ''
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
    global savedPreptime

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
            savedPreptime = request.form["preptime"]
            if request.form["ingredient_"+str(numOfIngredients-1)].strip() != '':
                savedIngredients.append(request.form["ingredient_"+str(numOfIngredients-1)])
                numOfIngredients += 1
        # Adds a step text field to the form
        if "add_step_bt" in request.form:
            savedLabel = request.form["recipename"]
            savedImageurl = request.form["imageurl"]
            savedPreptime = request.form["preptime"]
            if request.form["step_"+str(numOfSteps-1)].strip() != '':
                savedSteps.append(request.form["step_"+str(numOfSteps-1)])
                numOfSteps += 1
        # Submit the recipe to our database using the form fields
        if "submit_bt" in request.form:
            # Hope this doesn't hit already existed id when appended with userid
            rand = random.randint(1,10000)
            recipeId = str(authentication.userid) + "recipe" + str(rand)
            preptime = 0
            try:
                preptime = int(request.form["preptime"])
            except ValueError:
                pass

            ingredientList = []
            for i in range(numOfIngredients):
                ingredientList.append(textParser.seperateAlphaAndDigit(request.form["ingredient_"+str(i)]))
            database.add_recipe_ingredients_db(recipeId, ingredientList)

            ingredientString = ''
            # parse out ";" characters from all steps. This is because we will use ; to seperate the steps for storage in db
            for i in range(numOfSteps):
                tmp = textParser.filterCharacter(str(request.form["step_"+str(i)]), ";")
                ingredientString += (tmp + " ; ")

            database.add_recipe_overview_db(recipeId, authentication.userid, request.form["recipename"], request.form["imageurl"], preptime, ingredientString)

            return redirect(url_for("recipe", recipeId = recipeId))

    return render_template("uploadrecipe.html", numOfIngredients = numOfIngredients, numOfSteps = numOfSteps, savedIngredients = savedIngredients, savedSteps = savedSteps, savedLabel = savedLabel, savedImageurl = savedImageurl, savedPreptime = savedPreptime, userid = authentication.userid, userimage = authentication.imageurl)
