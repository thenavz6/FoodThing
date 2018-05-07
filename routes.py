from flask import *
import requests
import json
import random

app = Flask(__name__)

@app.route("/",methods=["GET", "POST"])
def main():
    if request.method == "POST":
        return redirect(url_for("dashboard"))
    return render_template("login.html")


# Had to make this ugly global variable to retain the same recipeId list in between the GET and POST
# Otherwise when the user clicked on a recipe, we were making the API requests again and this took the user to the wrong recipe.
recipeId = []
@app.route("/dashboard",methods=["GET", "POST"])
def dashboard():
    return searchRecipe("lol")


# Does essentially the same as the above. Except based on search query text - so the above should populate with random recipes.
@app.route("/searchRecipe/<query>", methods=["GET", "POST"])
def searchRecipe(query):

    global recipeId
    recipeLabels = []
    recipeImageLinks = []
    rand = random.randint(1,50)

    if request.method == "GET":
        response = requests.get("https://api.edamam.com/search?q="+str(query)+"&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca&from="+str(rand)+"&to="+str(rand+9))
        jsonData = response.json()["hits"]

        recipeId = []
        for item in jsonData:
            recipeId.append(item.get('recipe').get('uri'))
            recipeLabels.append(item.get('recipe').get('label'))
            recipeImageLinks.append(item.get('recipe').get('image'))

    if request.method == "POST":
        if request.form["bt"] == "Search" and request.form["searchtext"].strip() != "":
            return redirect(url_for("searchRecipe", query = request.form["searchtext"]))
        if request.form["bt"][:6] == "recipe":
            return redirect(url_for("recipe", recipeId = recipeId[int(request.form["bt"][7:])].split("_",1)[1]))

    return render_template("dashboard.html", labelList = recipeLabels, imageList = recipeImageLinks)


# The 'specific' recipe page that details instructions and ingredients.
# Later this should lead to the substitution pop-up box and so and so.
@app.route("/recipe/<recipeId>", methods=["GET", "POST"])
def recipe(recipeId):

    response = requests.get("https://api.edamam.com/search?r=\
http%3A%2F%2Fwww.edamam.com%2Fontologies%2Fedamam.owl%23recipe_"+str(recipeId)+"&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca")

    recipe = response.json()[0]
    recipeLabel = recipe.get('label')
    recipeImage = recipe.get('image')
    recipeIngredients = []
    for ingredient in recipe.get('ingredients'):
        recipeIngredients.append(ingredient.get('text'))

    return render_template("recipe.html", recipeLabel = recipeLabel, recipeImage = recipeImage, recipeIngredients = recipeIngredients)

