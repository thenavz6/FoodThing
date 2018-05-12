from flask import *
import requests
import json
import random

import authentication
import server
from server import app


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

    if (user == None):
        return redirect(url_for("error"))

    print(user)
    authentication.is_authenticated = True
    authentication.userid = int(user[0])
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
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    # If the 'random' search term is in the recipe name it is ideal since then dashboard items can be stored and picked from our database.
    return searchRecipe("food")


# Does essentially the same as the above. Except based on search query text - so the above should populate with random recipes.
@app.route("/searchRecipe/<query>", methods=["GET", "POST"])
def searchRecipe(query):
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    global recipeId
    recipeLabels = []
    recipeImageLinks = []
    rand = random.randint(1,50)

    if request.method == "GET":
        recipeId = []

        response = requests.get("https://api.edamam.com/search?q="+str(query)+"&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca&from="+str(rand)+"&to="+str(rand+9))
        if (response.status_code != 200):
            return redirect(url_for("error"))
        jsonData = response.json()["hits"]

        for item in jsonData:
            # Add the recipe_overview to the database so we can search this too
            server.add_recipe_overview_db(item.get('recipe').get('uri').split("_",1)[1], -1, item.get('recipe').get('label'), item.get('recipe').get('image'))
            recipeId.append(item.get('recipe').get('uri').split("_",1)[1])
            recipeLabels.append(item.get('recipe').get('label'))
            recipeImageLinks.append(item.get('recipe').get('image'))

        # Search the recipe_overview Database Table for matching labels and append hits from here too if we don't get 9 from Edamam.
        # Won't handle multi worded queries very well. Dealing with multi worded queries is a whole different problem too.
        for item in server.find_recipes_keyword(query):
            if len(recipeId) >= 9:
                break
            recipeId.append(item[0])
            recipeLabels.append(item[1])
            recipeImageLinks.append(item[2])

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
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    response = requests.get("https://api.edamam.com/search?r=\
http%3A%2F%2Fwww.edamam.com%2Fontologies%2Fedamam.owl%23recipe_"+str(recipeId)+"&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca")

    if (response.status_code != 200):
        return redirect(url_for("error"))

    recipe = response.json()[0]
    recipeLabel = recipe.get('label')
    recipeImage = recipe.get('image')
    recipeIngredients = []
    for ingredient in recipe.get('ingredients'):
        recipeIngredients.append(ingredient.get('text'))

    usersWhoCommented = []
    recipeComments = []
    for entry in server.get_recipe_comments(recipeId):
        recipeComments.append(entry[2])
        usersWhoCommented.append(server.find_user_by_id_db(int(entry[1])))
    print(usersWhoCommented)

    if request.method == "POST":
        if "bt" in request.form:
            if request.form["bt"] == 'logout':
                authentication.is_authenticated = False;
                return redirect(url_for("main"))
            if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
                return redirect(url_for("searchRecipe", query = request.form["searchtext"]))
            if request.form["bt"] == "comment":
                server.add_recipe_comment(recipeId, authentication.userid, request.form["commentText"])
                return redirect(url_for("recipe", recipeId = recipeId))
        if "user" in request.form:
            return redirect(url_for("userprofile", userId = int(request.form["user"])))

    return render_template("recipe.html", recipeLabel = recipeLabel, recipeImage = recipeImage, recipeIngredients = recipeIngredients, userid = authentication.userid, imageurl = authentication.imageurl, recipeComments = recipeComments, usersWhoCommented = usersWhoCommented)


# The page for viewing any user's profile
@app.route("/user/<userId>", methods=["GET", "POST"])
def userprofile(userId):
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    # Find the given user in the database or error for non-integer input
    try:
        userHit = server.find_user_by_id_db(int(userId))
    except ValueError as e:
        return redirect(url_for("error"))

    # Default name and image passed if user not found
    profilename = "No one lives here :("
    profileimage = "https://i.vimeocdn.com/portrait/1274237_300x300"

    if userHit != None:
        profilename = userHit[2]
        profileimage = userHit[3]

    if request.method == "POST":
        if request.form["bt"] == "Upload Recipe":
            return redirect(url_for("uploadRecipe"))  
        if request.form["bt"] == 'logout':
            authentication.is_authenticated = False;
            return redirect(url_for("main"))
        if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
            return redirect(url_for("searchRecipe", query = request.form["searchtext"]))

    return render_template("userprofile.html", profileid = userId, profilename = profilename, profileimage = profileimage, myuserid = authentication.userid, userimage = authentication.imageurl)


# The page for uploading user recipes
@app.route("/uploadRecipe", methods=["GET", "POST"])
def uploadRecipe():
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    return render_template("uploadrecipe.html")

