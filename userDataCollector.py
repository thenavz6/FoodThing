# Gets useful data for a user given the user's id and then 
# returns the data is the format of a dictionary

import database
import recipeDataCollector
import authentication

def getUserDictionary(userId):
    # Default name and image passed if user not found
    profilename = "No one lives here :("
    profileimage = "https://i.vimeocdn.com/portrait/1274237_300x300"
    profiledesc = "How lonely"
    profilefavourites = []
    profilerecipes = []
    shoppingLists = []

    try:
        userHit = database.find_user_by_id_db(int(userId))
        # Load parameters based on database result
        if userHit != None:
            profilename = userHit["fullname"]
            profileimage = userHit["imageurl"]
            profiledesc = userHit["description"]
            profilefavourites = []
    
            shoppingLists = database.get_user_shopping_lists(userId)     

            findfavourites = database.find_user_favourites_db(userId)
            tmp = []
            searchScore = []
            for favourite in findfavourites:
                tmp.append(favourite["recipeID"])
                searchScore.append(0)
            profilefavourites = recipeDataCollector.getRecipeDictionaries(tmp, searchScore, authentication.userid, None)

            findRecipes = database.find_user_recipes_db(userId) 
            tmp = []
            searchScore = []
            for recipe in findRecipes:
                tmp.append(recipe["recipeID"])
                searchScore.append(0)
            profilerecipes = recipeDataCollector.getRecipeDictionaries(tmp, searchScore, authentication.userid, None)
                  
    except ValueError as e:
        pass

    profileuser = {
        "id"   : userId,
        "name" : profilename,
        "image": profileimage,
        "desc" : profiledesc,
        "profilefavourites" : profilefavourites,
        "profilerecipes" : profilerecipes,
        "shoppingLists" : shoppingLists
    }

    return profileuser
