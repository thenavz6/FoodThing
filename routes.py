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
    authentication.is_authenticated = True
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

    return searchRecipe("lol")


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
        response = requests.get("https://api.edamam.com/search?q="+str(query)+"&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca&from="+str(rand)+"&to="+str(rand+9))
        if (response.status_code != 200):
            return redirect(url_for("error"))
        jsonData = response.json()["hits"]

        recipeId = []
        for item in jsonData:
            recipeId.append(item.get('recipe').get('uri'))
            recipeLabels.append(item.get('recipe').get('label'))
            recipeImageLinks.append(item.get('recipe').get('image'))

    if request.method == "POST":
        if request.form["bt"] == 'logout':
            authentication.is_authenticated = False;
            return redirect(url_for("main"))
        if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
            return redirect(url_for("searchRecipe", query = request.form["searchtext"]))
        if request.form["bt"][:6] == "recipe":
            return redirect(url_for("recipe", recipeId = recipeId[int(request.form["bt"][7:])].split("_",1)[1]))

    return render_template("dashboard.html", labelList = recipeLabels, imageList = recipeImageLinks, imageurl = authentication.imageurl)


# The 'specific' recipe page that details instructions and ingredients.
# Later this should lead to the substitution pop-up box and so and so.
@app.route("/recipe/<recipeId>", methods=["GET", "POST"])
def recipe(recipeId):
    if authentication.is_authenticated == False:
        return redirect(url_for("main"))

    response = requests.get("https://api.edamam.com/search?r=\
http%3A%2F%2Fwww.edamam.com%2Fontologies%2Fedamam.owl%23recipe_"+str(recipeId)+"&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca")

    recipe = response.json()[0]
    recipeLabel = recipe.get('label')
    recipeImage = recipe.get('image')
    recipeIngredients = []
    for ingredient in recipe.get('ingredients'):
        recipeIngredients.append(ingredient.get('text'))

    if request.method == "POST":
        if request.form["bt"] == 'logout':
            authentication.is_authenticated = False;
            return redirect(url_for("main"))
        if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
            return redirect(url_for("searchRecipe", query = request.form["searchtext"]))

    return render_template("recipe.html", recipeLabel = recipeLabel, recipeImage = recipeImage, recipeIngredients = recipeIngredients, imageurl = authentication.imageurl)

