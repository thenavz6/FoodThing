from flask import *
import requests
import json

import authentication
import server
from server import app
import database
import textParser
import searchRecipes
import productFinder
import costCalculator
import recipeDataCollector
import userDataCollector
from helperFunctions import *


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


# We need to verify this token with Google for security.
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
recipeHitScore = []
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

    return advancedSearch(query, None, None, None)


numOfExcluded = 1
excludedIngredients = []
@app.route("/advancedSearchPage", methods=["GET", "POST"])
def advancedSearchPage():
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    global numOfExcluded, excludedIngredients

    if request.method == "GET":
        numOfExcluded, excludedIngredients = 1, []

    if request.method == "POST":
        if headerRequests(request.form) != None:
            return headerRequests(request.form)
        if request.form["srchbt"] == "Search":
            query = request.form["KeyWords"]
            excluded = request.form["Exclude"]
            prepTime = request.form["MaxPrepTime"]
            cost = request.form["MaximumCost"]
            if request.form["KeyWords"] == "":
                query = "empty"
            if request.form["Exclude"] == "":
                excluded = "empty"
            if request.form["MaxPrepTime"] == "":
                prepTime = "empty"
            if request.form["MaximumCost"] == "":
                cost = "empty"
            return redirect(url_for("advancedSearch", query = query, excluded = excluded, prepTime = prepTime, cost = cost))

    return render_template("advancedSearch.html", numOfExcluded = numOfExcluded,excludedIngredients = excludedIngredients)


@app.route("/advancedSearch/<query>/<excluded>/<prepTime>/<cost>", methods=["GET", "POST"])
def advancedSearch(query,excluded,prepTime,cost):
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    global recipeId, recipeHitScore, recipes, sortType

    if request.method == "GET":
        sortedRecipes = searchRecipes.getRecipes(query, excluded, prepTime, cost)
        sortedRecipes = sortedRecipes[:9]
        recipeId, recipeHitScore = [], []
        for recipe in sortedRecipes:
            recipeId.append(recipe[0])
            recipeHitScore.append(recipe[1])
        recipes = recipeDataCollector.getRecipeDictionaries(recipeId, recipeHitScore, authentication.userid, None)
        sortType = "Relevance"

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
        if "favbt" in request.form:
            database.add_user_favourite_db(authentication.userid, request.form["favbt"])
            return redirect(url_for("userprofile", userId = authentication.userid))
        if "unfavbt" in request.form:
            database.delete_user_favourite_db(authentication.userid, request.form["unfavbt"])
            return redirect(url_for("userprofile", userId = authentication.userid))
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
    userShoppingList = database.get_user_shopping_list(authentication.userid, recipeId)

    # First check if we have this recipe in our database already which will be true if it appeared in a search query
    # Makes future requests (like favouriting and commenting MUCH FASTER)
    recipeHit = database.find_recipe_id_db(recipeId)
    if recipeHit == []:
        recipeDataCollector.recieveSingleRecipe(recipeId)
        recipeHit = database.find_recipe_id_db(recipeId)

    if request.method == "GET":
      # If the user has saved this recipe as a Shopping List
        if userShoppingList != None:
            selectedProducts = []
            tmp = userShoppingList
            userShoppingList = tmp["selectedProducts"]
            prefStore = tmp["selectedStore"]
            userShoppingList = userShoppingList.split(",")
            for product in userShoppingList:
                selectedProducts.append(int(product))

        recipeDict = recipeDataCollector.getRecipeDictionaries([recipeId], [0], authentication.userid, prefStore)[0]

        # By default if this isn't a shopping list we select the cheapest, most relevent products
        if userShoppingList == None:
            selectedProducts = []
            for ingredient in recipeDict["ingredients"]:
                selectedProducts.append(0)

        # Increase the recipe's clickCount/popularity in the recipe overview TABLE
        database.increment_recipe_clickcount_db(recipeId)

    # Calculate the total effective price based on the selectedProducts
    totalEffectiveCost = costCalculator.calcTotalCost(recipeDict, selectedProducts)
    totalRealCost = costCalculator.calcTotalRealCost(recipeDict, selectedProducts)

    # Retrieve all comments and the users who left those comments
    usersWhoCommented = []
    recipeComments = []
    for entry in database.get_recipe_comments_db(recipeId):
        recipeComments.append(entry["comment"])
        usersWhoCommented.append(database.find_user_by_id_db(int(entry["userID"])))

    # Get what the current user has rated this recipe
    userRating = database.find_user_rating_db(authentication.userid, recipeId)
    if userRating == None:
        userRating = -1
    else:
        userRating = int(userRating["rating"])

    # Possible post requests
    if request.method == "POST":
        if headerRequests(request.form) != None:
            return headerRequests(request.form)
        if recipeCardRequests(request.form) != None:
            return redirect(url_for("recipe", recipeId = recipeId))
        if "commentbt" in request.form:
            database.add_recipe_comment_db(recipeId, authentication.userid, request.form["commentText"])
            return redirect(url_for("recipe", recipeId = recipeId))
        if "favbt" in request.form:
            database.add_user_favourite_db(authentication.userid, request.form["favbt"])
            return redirect(url_for("recipe", recipeId = recipeId))
        if "unfavbt" in request.form:
            database.delete_user_favourite_db(authentication.userid, request.form["unfavbt"])
            return redirect(url_for("recipe", recipeId = recipeId))
        if "ratingbt" in request.form:
            database.add_user_rating_db(authentication.userid, recipeId, request.form["ratingbt"])
            return redirect(url_for("recipe", recipeId = recipeId))
        if "user" in request.form:
            return redirect(url_for("userprofile", userId = int(request.form["user"])))
        if "storebt" in request.form:
            prefStore = request.form["selectstore"]
            recipeDict = recipeDataCollector.getRecipeDictionaries([recipeId], [0], authentication.userid, prefStore)[0]
            # Reset product preferences
            for i in range(0, len(selectedProducts)):
                selectedProducts[i] = 0
            # Recalculate the total effective price based on the selectedProducts
            totalEffectiveCost = costCalculator.calcTotalCost(recipeDict, selectedProducts)
            totalRealCost = costCalculator.calcTotalRealCost(recipeDict, selectedProducts)
        if "productbt" in request.form:
            selectedProducts[int(request.form["productbt"].split("_")[0])] = int(request.form["productbt"].split("_")[1])
            # Recalculate the total effective price based on the selectedProducts
            totalEffectiveCost = costCalculator.calcTotalCost(recipeDict, selectedProducts)
            totalRealCost = costCalculator.calcTotalRealCost(recipeDict, selectedProducts)
        if "shoppingbt" in request.form:
            print(selectedProducts)
            database.update_user_shopping_list(authentication.userid, recipeId, selectedProducts, prefStore, totalEffectiveCost, totalRealCost)
            return redirect(url_for("recipe", recipeId = recipeId))

    return render_template("recipe.html", recipeDict = recipeDict, prefStore = prefStore, selectedProducts = selectedProducts, totalEffectiveCost = "%0.2f" % totalEffectiveCost, totalRealCost = "%0.2f" % totalRealCost, steps = recipeDict["instructions"].split(";")[:-1], userid = authentication.userid, imageurl = authentication.imageurl, recipeComments = recipeComments, usersWhoCommented = usersWhoCommented, userRating = userRating, userShoppingList = userShoppingList)


# The page for viewing any user's profile
@app.route("/user/<userId>", methods=["GET", "POST"])
def userprofile(userId):
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    sumEffectiveCost = 0
    sumRealCost = 0
    profileuser = userDataCollector.getUserDictionary(userId)
    for item in profileuser["shoppingLists"]:
        sumEffectiveCost += float(item["effectiveCost"])
        sumRealCost += float(item["realCost"])
    

    # Possible post requests
    if request.method == "POST":
        if headerRequests(request.form) != None:
            return headerRequests(request.form)
        if "favbt" in request.form:
            database.add_user_favourite_db(authentication.userid, request.form["favbt"])
            return redirect(url_for("userprofile", userId = authentication.userid))
        if "unfavbt" in request.form:
            database.delete_user_favourite_db(authentication.userid, request.form["unfavbt"])
            return redirect(url_for("userprofile", userId = authentication.userid))
        if "bt" in request.form:
            if request.form["bt"] == "Upload Recipe":
                return redirect(url_for("uploadRecipe"))
            if request.form["bt"] == "UpdateDesc":
                database.set_desc_user_db(authentication.userid, request.form["updatedesc"])
                return redirect(url_for("userprofile", userId = userId))

    return render_template("userprofile.html", profileuser = profileuser, getRecipeDictionaries = recipeDataCollector.getRecipeDictionaries, userid = authentication.userid, userimage = authentication.imageurl, sumEffectiveCost = sumEffectiveCost, sumRealCost = sumRealCost)


# Global variables to preserve between post calls
savedLabel, savedImageurl, savedPreptime, savedDesc = '', '', '', ''
numOfIngredients, numOfSteps = 1, 1
savedIngredients, savedSteps = [], []
# The page for uploading user recipes
@app.route("/uploadRecipe", methods=["GET", "POST"])
def uploadRecipe():
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    global numOfIngredients, numOfSteps, savedIngredients, savedSteps
    global savedLabel, savedImageurl, savedPreptime, savedDesc

    # Reset the number of ingredients and steps for this page
    if request.method == "GET":
        savedLabel, savedImageurl, savedPreptime, savedDesc = '', '', '', ''
        numOfIngredients, numOfSteps = 1, 1
        savedIngredients, savedSteps = [], []

    if request.method == "POST":
        if headerRequests(request.form) != None:
            return headerRequests(request.form)
        # Adds an ingredient text field to the form
        if "add_ingred_bt" in request.form:
            savedLabel = request.form["recipe_name"]
            savedImageurl = request.form["imageurl"]
            savedPreptime = request.form["recipe_preptime"]
            savedDesc = request.form["recipe_desc"]
            savedIngredients = []
            for i in range(0, numOfIngredients):
                savedIngredients.append(request.form["ingredient_"+str(i)])
            savedSteps = []
            for i in range(0, numOfSteps):
                savedSteps.append(request.form["step_"+str(i)])
            numOfIngredients += 1
        # Adds a step text field to the form
        if "add_step_bt" in request.form:
            savedLabel = request.form["recipe_name"]
            savedImageurl = request.form["imageurl"]
            savedPreptime = request.form["recipe_preptime"]
            savedDesc = request.form["recipe_desc"]
            savedIngredients = []
            for i in range(0, numOfIngredients):
                savedIngredients.append(request.form["ingredient_"+str(i)])
            savedSteps = []
            for i in range(0, numOfSteps):
                savedSteps.append(request.form["step_"+str(i)])
            numOfSteps += 1
        # Submit the recipe to our database using the form fields
        if "add_recipe_bt" in request.form:
            # Check if the form is sufficiently filled
            if request.form["recipe_name"].strip() != '' and request.form["ingredient_0"].strip() != '' and request.form["step_0"].strip() != '':
                # Hope this doesn't hit already existed id when appended with userid
                rand = random.randint(1,10000)
                recipeId = str(authentication.userid) + "recipe" + str(rand)
                preptime = 0
                try:
                    preptime = int(request.form["recipe_preptime"])
                except ValueError:
                    pass

                ingredientList = []
                for i in range(numOfIngredients):
                    if request.form["ingredient_"+str(i)].strip() != "":
                        ingredientList.append(textParser.seperateAlphaAndDigit(request.form["ingredient_"+str(i)]))
                database.add_recipe_ingredients_db(recipeId, ingredientList)

                ingredientString = ''
                # parse out ";" characters from all steps. This is because we will use ; to seperate the steps for storage in db
                for i in range(numOfSteps):
                    if request.form["step_"+str(i)].strip() != "":
                        tmp = textParser.filterCharacter(str(request.form["step_"+str(i)]), ";")
                        ingredientString += (tmp + " ; ")

                # Default recipe image if none supplied
                recipeimage = request.form["imageurl"]
                if request.form["imageurl"].strip() == "":
                    recipeimage = "https://i.gifer.com/C2D6.gif"

                database.add_recipe_overview_db(recipeId, authentication.userid, request.form["recipe_name"], recipeimage, preptime, ingredientString, request.form["recipe_desc"], 0, [])

                return redirect(url_for("recipe", recipeId = recipeId))

    return render_template("addRecipe.html", numOfIngredients = numOfIngredients, numOfSteps = numOfSteps, savedIngredients = savedIngredients, savedSteps = savedSteps, savedLabel = savedLabel, savedImageurl = savedImageurl, savedPreptime = savedPreptime, savedDesc = savedDesc, userid = authentication.userid, userimage = authentication.imageurl)
