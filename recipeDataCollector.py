# Given a list of recipeIDs this will return a list of RecipeDictionaries
# Each Dictionary having format:
# {"id" : recipeId, "name" : recipeName, "image" : urllink, "rating" : rating, , "preptime" : preptime, "isfav" : has the user favourited this?, "cost" : est. best cost}
# This dictionary should contain any desirable data for a recipe

import requests
import json
import database
import productFinder
import costCalculator
import random

def getRecipeDictionaries(recipeIDList, userId):
    dictionaryList = []
    for recipeId in recipeIDList:
        # Find the recipe overview from the recipe_overview TABLE
        overviewEntry = database.find_recipe_id_db(recipeId)

        # Find all relevent product hits for each ingredient for this recipe
        ingredientProducts = []
        recipeIngredients = database.find_recipe_ingredients_db(recipeId)
        for ingredient in recipeIngredients:
            ingredientProducts.append(productFinder.findBestProducts(ingredient))
        estcost = costCalculator.calcBestCost(ingredientProducts)

        recipeDict = {
            "id" : recipeId,
            "name" : overviewEntry["recipeLabel"],
            "image": overviewEntry["recipeImageLink"],
            "ingredients" : recipeIngredients,                  # Each ingredient etc. "eggs"
            "ingredientProducts" : ingredientProducts,          # Each product that hit the above ingredient, etc. "12pk eggs", "free range eggs"
            "rating" : overviewEntry["recipeRating"],
            "preptime": "???" if (float(overviewEntry["prepTime"]) == 0) else str(overviewEntry["prepTime"]),
            "isfav" : database.is_user_favourited_db(userId, recipeId),
            "effectiveCost" : estcost["effectiveCost"],
            "totalCost" : estcost["totalCost"]
         }
        
        dictionaryList.append(recipeDict)

    return dictionaryList


# The below function will ask edamam for num amount of recipe's and then store the data recieved 
# into our local database. Returns whether edamam was successfully contacted.
def receiveRecipeData(queryString, num, exclusionQuery, prepTime):
    rand = random.randint(1,50)
    requestString = "https://api.edamam.com/search?q="+str(queryString)+"&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca&from="+str(rand)+"&to="+str(rand+num)
    if exclusionQuery != None:
        requestString += "&excluded="+exclusionQuery
    if prepTime != None:
        requestString += "&time="+prepTime

    response = requestString
    if response.status_code != 200:
        return False
    
    # For each recipe we get back, we add them to our local database if they aren't there already
    jsonData = response.json()["hits"]
    for item in jsonData:
        if database.add_recipe_overview_db(item.get('recipe').get('uri').split("_",1)[1], -1, item.get('recipe').get('label'), item.get('recipe').get('image'), item.get('recipe').get('totalTime')) != -1:
            recipeIngredients = []
            for ingredient in item.get('recipe').get('ingredients'):
                recipeIngredients.append(ingredient.get('text'))
            database.add_recipe_ingredients_db(item.get('recipe').get('uri').split("_",1)[1], recipeIngredients)

    return True

    
# Will ask edamam for the details for a recipe with the givenId and then save locally. Returns
# sucess of contacting edamam
def recieveSingleRecipe(recipeId):
    response = requests.get("https://api.edamam.com/search?r=\
http%3A%2F%2Fwww.edamam.com%2Fontologies%2Fedamam.owl%23recipe_"+str(recipeId)+"&app_id=c565299e&app_key=\
b90e6fb2878260b8f991bd4f9a8663ca")
    if response.status_code != 200:
        return False
    
    recipe = response.json()[0]
    recipeIngredients = []
    for ingredient in recipe.get('ingredients'):
        recipeIngredients.append(ingredient.get('text'))
    database.add_recipe_overview_db(recipeId, -1, recipe.get('label'), recipe.get('image'), recipe.get('totalTime'))
    database.add_recipe_ingredients_db(recipeId, recipeIngredients)

    return True
    


