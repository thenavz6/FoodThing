from flask import *
import requests
import json

app = Flask(__name__)

@app.route("/",methods=["GET", "POST"])
def main():
    if request.method == "POST":
        return redirect("/home")
    else:
        return render_template("login.html")

@app.route("/home",methods=["GET", "POST"])
def home():
    response = requests.get("https://api.edamam.com/search?q=chicken&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca&from=0&to=9")
    print(response.json())
    return render_template("home.html")
