# For one recipe, given the list of ingredientProducts, this aims (see Recipe in Routes.py)
# to determine the cheapest cost while still maintaining relevent products

def calcBestCost(ingredientProducts):
    # TODO possible change the hitScore to a range, right now only looks at products with == highestHitScore
    bestHitCost = 0
    bestHitPortionCost = 0
    for products in ingredientProducts:
        # Get the highestHitScore for this ingredient
        try:
            highestHitScore = products[0]["hitScore"]
        except IndexError:
            continue

        lowestPortionPrice = 99999
        matchingFullPrice = 99999

        for product in products:

            if product["hitScore"] == highestHitScore:
                if product["effectiveCost"] < lowestPortionPrice:
                    lowestPortionPrice = product["effectiveCost"] 
                    matchingFullPrice = product["realCost"]
        bestHitPortionCost += float(lowestPortionPrice)
        bestHitCost += float(matchingFullPrice)

    return {"effectiveCost" : "%0.2f" % bestHitPortionCost, "totalCost" : "%0.2f" % bestHitCost}
    

# Calculate the total EFFECTIVE cost of selected products which may or may not be the cheapest
# selectedProducts in a list of incidicies describing which number product has been selected for a given ingredient
def calcTotalCost(recipeDict, selectedProducts):
    totalEffectiveCost, i = 0, 0
    for ingredient in recipeDict["ingredients"]:
        try:
            totalEffectiveCost += recipeDict["ingredientProducts"][i][selectedProducts[i]]["effectiveCost"]
        except IndexError:
            pass
        i += 1
    return totalEffectiveCost


def calcTotalRealCost(recipeDict, selectedProducts):
    totalRealCost, i = 0, 0
    for ingredient in recipeDict["ingredients"]:
        try:
            print(recipeDict["ingredientProducts"][i][selectedProducts[i]])
            totalRealCost += recipeDict["ingredientProducts"][i][selectedProducts[i]]["realCost"] 
        except IndexError:
            pass
        i += 1
    return totalRealCost

