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


@app.route("/dashboard",methods=["GET", "POST"])
def dashboard():

    recipeLabels = []
    recipeImageLinks = []
    rand = random.randint(1,50)

    response = requests.get("https://api.edamam.com/search?q=lol&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca&from="+str(rand)+"&to="+str(rand+9))

    jsonData = response.json()["hits"]

    for item in jsonData:
        recipeLabels.append(item.get('recipe').get('label'))
        recipeImageLinks.append(item.get('recipe').get('image'))

    print(recipeLabels)
    print(recipeImageLinks)

    if request.method == "POST":
        print(request.form)
        return redirect(url_for("searchRecipe", query = request.form["searchtext"]))

    return render_template("dashboard.html", labelList = recipeLabels, imageList = recipeImageLinks)


# Does essentially the same as the above. Except based on search query text
# TODO Make the code recallable where its common with the above
@app.route("/searchRecipe/<query>", methods=["GET", "POST"])
def searchRecipe(query):

    recipeLabels = []
    recipeImageLinks = []
    rand = random.randint(1,50)

    response = requests.get("https://api.edamam.com/search?q="+str(query)+"&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca&from="+str(rand)+"&to="+str(rand+9))

    jsonData = response.json()["hits"]

    for item in jsonData:
        recipeLabels.append(item.get('recipe').get('label'))
        recipeImageLinks.append(item.get('recipe').get('image'))

    print(recipeLabels)
    print(recipeImageLinks)

    if request.method == "POST":
        print(request.form)
        return redirect(url_for("searchRecipe", query = request.form["searchtext"]))

    return render_template("dashboard.html", labelList = recipeLabels, imageList = recipeImageLinks)

