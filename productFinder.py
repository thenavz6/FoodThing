import database
import ingredientManager
import textParser
import math

# Converts all given terms to GRAMS to standardize comparison between different measures
unitConverter = {
    'cup': 220.0,
    'tablespoon': 15.0,
    'teaspoon': 5.0,
    'ounce' : 28.0,
    'gram' : 1.0,
    'milligram' : 0.001,
    'kilogram' : 1000.0,
    'dash' : 0.1,
    'pinch' : 0.3,
    'pound' : 453.6, 
    'pint' : 473.2,
    'quart' : 946.4,
    'gallon' : 4405.0,
    'milliliter' : 1.0,
    'liter' : 1000.0,
    'unit' : 1.0
}

# Parameter: The ingredient entry from the database: recipe_ingredients
# Returns the best, most relevent products for this ingredient
# Also considers conversions and costs etc.
def findBestProducts(ingredient):
    # Dictionary that stores how many hits a given product has. etc 'product12' : 5, 'product2' : 2
    productHits = {}

    wordsInIngredient = 0
    for word in ingredient["item"].split():
        if word.isalpha() and not word.lower() in textParser.commonWords and not word.lower() in textParser.brandNames:
            wordsInIngredient += 1   

    # For each keyword etc. 'sour cream buttermilk' we want to search the product database
    for word in ingredient["item"].split():
        # Remove possible plural from end of ingredient keyword. DB products have the same applied, so matches still hit.
        if len(word) > 3:
            if word.endswith('es'):
                word = word[:-2]
            elif word.endswith('s'):
                word = word[:-1]

        products = database.find_products_keyword_db(word)
        # Get the product from from it's overview table
        for product in products:

            productDbEntry = database.get_product_overview_db(product["productID"])
            # Every hit product will have a score of 1 added to it 
            # Check if we have seen this productID/product before
            if product["productID"] in productHits:
                productHits[product["productID"]] += 1
            else:
                productHits.update({product["productID"] : 1})

        for key, value in productHits.items():
            # Calculate the number of words in the products name to adjust hit score
            productDbEntry = database.get_product_overview_db(key)
            wordsInName = 0
            for word in productDbEntry["label"].split():
                if word.isalpha() and not word in textParser.commonWords and not word in textParser.brandNames:
                    wordsInName += 1
            productHits[key] = (float(value)) / (float(wordsInIngredient) * float(wordsInName))

    # Sort the product hits based on hitscore and cap the number of product results
    sortedProducts = sorted(productHits.items(), key=lambda x : x[1], reverse=True)
    sortedProducts = capNumberOfResults(sortedProducts, 20)
    detailList = convertToDetailList(sortedProducts, ingredient)
    return detailList


def capNumberOfResults(sortedProducts, limit):
    return sortedProducts[:limit]


# Turns the sortedProduct Dictionary into a list of lists that contains all properties of the product 
# Each item in the list refers to a specific product for that ingredient. Each sublist contains detailed
# information about that product. Takes in the general recipe_ingredient entry as second parameter to evaluate portion cost
def convertToDetailList(sortedProducts, ingredient):
    productList = []
    for item in sortedProducts:
        productOverview = database.get_product_overview_db(item[0])

        # Standardize all measures to grams 
        standardizedUnit1 = ingredientManager.findKeyFromMeasureDict(productOverview["unit"])
        gramMeasure1 = convertAmountToGram(productOverview["quantity"], standardizedUnit1)
        standardizedUnit2 = ingredient["measure"]
        gramMeasure2 = convertAmountToGram(ingredient["quantity"], ingredient["measure"])
    
        # Calculate how many portions are needed (etc. 0.25 of that item or 2 of these items)
        portionCost = 0
        if productOverview["unit"] == "unit" and ingredient["measure"] == "unit":
            portionCost = float(productOverview["cost"]) * (float(ingredient["quantity"]) / float(productOverview["quantity"]))
        elif productOverview["unit"] == "unit" or ingredient["measure"] == "unit":
            portionCost = float(productOverview["cost"])
        else:
            portionCost = (gramMeasure2 / gramMeasure1) * float(productOverview["cost"])
            # If we need to buy more than 5 of these, probably a better product...
            if gramMeasure2/gramMeasure1 > 5.02:
                continue

        # The real cost is the base cost * the ceiling of the portions. 
        # Etc. If we need 500mL and this means we need 1.5 portions of a product, we need to actually buy 2.
        realCost = float(productOverview["cost"]) * math.ceil(portionCost / float(productOverview["cost"]))
       

        productDict = {"productID" : item[0], "hitScore" : item[1], "label" : productOverview["label"], "quantity" : productOverview["quantity"], "unit" : standardizedUnit1, "cost" : productOverview["cost"], "grams" : gramMeasure1, "unitCost" : productOverview["cost"], "realCost" : realCost, "effectiveCost" : portionCost, "image" : productOverview["imagelink"]}
        productList.append(productDict)
    return productList


# Converts the given quantity and unit to grams, etc. 5 pounds = x grams
def convertAmountToGram(quantity, unit):
    return float(quantity) *  unitConverter[str(unit)]


