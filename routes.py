from flask import *
import requests
import json
import random

app = Flask(__name__)

@app.route("/",methods=["GET", "POST"])
def main():
    if request.method == "POST":
        return redirect("/home")
    else:
        return render_template("login.html")

@app.route("/home",methods=["GET", "POST"])
def home():

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

    return render_template("home.html", labelList = recipeLabels, imageList = recipeImageLinks)
