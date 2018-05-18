# For one recipe, given the list of ingredientProducts, this aims (see Recipe in Routes.py)
# to determine the cheapest cost while still maintaining relevent products

def calcBestCost(ingredientProducts):
    # TODO change the hitScore to a range, right now only looks at products with == highestHitScore
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
                if product["portionCost"] < lowestPortionPrice:
                    lowestPortionPrice = product["portionCost"] 
                    matchingFullPrice = product["cost"]
        bestHitPortionCost += float(lowestPortionPrice)
        bestHitCost += float(matchingFullPrice)

    print("Bill is: " + str(bestHitCost))
    print("The recipe takes: " + str(bestHitPortionCost))
    
