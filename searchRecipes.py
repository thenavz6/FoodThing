# This contains functions that are related to the search and advancedSearch routes

import database
import recipeDataCollector

OFFLINEMODE = False

# query is the query string that may be multi-worded "Scrambled Eggs"
# excluded is a list of ingredients to exclude etc ["nuts", "salmon"]
def getRecipes(query, excluded, preptime, cost):

    global OFFLINEMODE

    # Everytime a search is done, we will ask edamam for 5 recipes that we also add locally
    # Edamam handles multi worded queries for us
    if (OFFLINEMODE == False):
        recipeDataCollector.receiveRecipeData(query, 5, excluded, preptime)

    # Store as the key the recipeId and the value the number of hits
    recipeHits = {}

    query = query.split()
    for keyword in query:
        # Run different database query for normal search or advanced search
        hitRecipeIds = []
        if keyword == "random":
            hitRecipeIds = database.get_random_recipes_db(9)
        elif excluded == None:
            hitRecipeIds = database.find_recipes_keyword_db(keyword)
        else:
            hitRecipeIds = database.find_recipes_overview_db(keyword, excluded, preptime, cost)

        # If we found hits, then for each recipeId hit increment its count in the hit dictionary
        if hitRecipeIds != []:
            for hitRecipe in hitRecipeIds:
                hitRecipe["recipeID"]

                # Check if we already have recorded the recipeID as a hit before
                if hitRecipe["recipeID"] in recipeHits:
                    recipeHits[hitRecipe["recipeID"]] += 1
                else:
                    recipeHits.update({hitRecipe["recipeID"] : 1})

    # After checking each keyword and building the hitDictionary, we need to order based on hitcount
    sortedRecipes = sorted(recipeHits.items(), key=lambda x : x[1], reverse=True)

    return sortedRecipes
