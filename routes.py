from flask import *
import requests
import json

import authentication
import server
from server import app
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
    server.update_user_db(request.form['email'], request.form['fullname'], request.form['imageurl'], request.form['token'])
    user = server.find_user_by_email_db(request.form['email'])

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
        databaseRecipes = server.find_recipes_keyword_db(query)
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
            if server.add_recipe_overview_db(item.get('recipe').get('uri').split("_",1)[1], -1, item.get('recipe').get('label'), item.get('recipe').get('image')) != -1:
                server.add_recipe_ingredients_db(item.get('recipe').get('uri').split("_",1)[1], recipeIngredients)

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
    recipeLabel, recipeImage, recipeIngredients = "", "", []

    # First check if we have this recipe in our database already which will be true if it appeared in a search query
    # Makes future requests (like favouriting and commenting MUCH FASTER)
    recipeHit = server.find_recipe_id_db(recipeId)
    if recipeHit != None:
        recipeLabel = recipeHit["recipeLabel"]
        recipeImage = recipeHit["recipeImageLink"]
        for ingredient in server.find_recipe_ingredients_db(recipeId):
            recipeIngredients.append(ingredient["ingredientDesc"])

    # Only if we do not have it in the db then we ask edamam
    else:
        response = requests.get("https://api.edamam.com/search?r=\
    http%3A%2F%2Fwww.edamam.com%2Fontologies%2Fedamam.owl%23recipe_"+str(recipeId)+"&app_id=c565299e&app_key=\
    b90e6fb2878260b8f991bd4f9a8663ca")

        if (response.status_code != 200):
            return redirect(url_for("error"))
        recipe = response.json()[0]
        recipeLabel = recipe.get('label')
        recipeImage = recipe.get('image')
        for ingredient in recipe.get('ingredients'):
            recipeIngredients.append(ingredient.get('text'))
        # Also add the recipe to the db since we didn't have it
        server.add_recipe_overview_db(recipeId, -1, recipeLabel, recipeImage)
        server.add_recipe_ingredients_db(recipeId, recipeIngredients)

    # Check if the user has favourited this recipe
    isFavourited = False
    userFavourites = server.find_user_favourites_db(authentication.userid)
    for favourite in userFavourites:
        if recipeId == favourite["recipeID"]:
            isFavourited = True

    # Retrieve all comments and the users who left those comments
    usersWhoCommented = []
    recipeComments = []
    for entry in server.get_recipe_comments_db(recipeId):
        recipeComments.append(entry["comment"])
        usersWhoCommented.append(server.find_user_by_id_db(int(entry["userID"])))

    # Possible post requests
    if request.method == "POST":
        if "bt" in request.form:
            if request.form["bt"] == 'logout':
                authentication.is_authenticated = False;
                return redirect(url_for("main"))
            if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
                return redirect(url_for("searchRecipe", query = request.form["searchtext"]))
            if request.form["bt"] == "comment":
                server.add_recipe_comment_db(recipeId, authentication.userid, request.form["commentText"])
                return redirect(url_for("recipe", recipeId = recipeId))
            if request.form["bt"] == "Favourite":
                server.add_user_favourite_db(authentication.userid, recipeId)
                return redirect(url_for("recipe", recipeId = recipeId))
            if request.form["bt"] == "Unfavourite":
                server.delete_user_favourite_db(authentication.userid, recipeId)
                return redirect(url_for("recipe", recipeId = recipeId))
        if "user" in request.form:
            return redirect(url_for("userprofile", userId = int(request.form["user"])))

    return render_template("recipe.html", recipeId = recipeId, recipeLabel = recipeLabel, recipeImage = recipeImage, recipeIngredients = recipeIngredients, userid = authentication.userid, imageurl = authentication.imageurl, isFavourited = isFavourited, recipeComments = recipeComments, usersWhoCommented = usersWhoCommented)


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

    # Find the given user in the database or error for non-integer input
    try:
        userHit = server.find_user_by_id_db(int(userId))
    except ValueError as e:
        return redirect(url_for("error"))

    # Load parameters based on database result
    if userHit != None:
        profilename = userHit["fullname"]
        profileimage = userHit["imageurl"]
        profilefavourites = []
        findfavourites = server.find_user_favourites_db(userId)
        for favourite in findfavourites:
            profilefavourites.append(favourite["recipeID"])

    # Possible post requests
    if request.method == "POST":
        if request.form["bt"] == "Upload Recipe":
            return redirect(url_for("uploadRecipe"))
        if request.form["bt"] == 'logout':
            authentication.is_authenticated = False;
            return redirect(url_for("main"))
        if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
            return redirect(url_for("searchRecipe", query = request.form["searchtext"]))

    return render_template("userprofile.html", profileid = userId, profilename = profilename, profileimage = profileimage, profilefavourites = profilefavourites, myuserid = authentication.userid, userimage = authentication.imageurl)


# The page for uploading user recipes
@app.route("/uploadRecipe", methods=["GET", "POST"])
def uploadRecipe():
    # Ensure the user is logged in
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    return render_template("uploadrecipe.html")

