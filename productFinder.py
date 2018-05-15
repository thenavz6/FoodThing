import server
import ingredientManager

# Converts all given terms to GRAMS to standardize comparison between different measures
unitConverter = {
    'cup': 230.0,
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

# Parameter: The ingredient entry from the databse
# Returns the best, most relevent products for this ingredient
# Also considers conversions and costs etc.
def findBestProducts(ingredient):
    # Dictionary that stores how many hits a given product has. etc 'product12' : 5, 'product2' : 2
    productHits = {}

    # For each keyword etc. 'sour cream buttermilk' we want to search the product database
    for word in ingredient["item"].split():
        products = server.find_products_keyword_db(word)
        # Get the product from from it's overview table
        for product in products:
            wordsInLabel = len(server.get_product_overview_db(product["productID"])["label"])
            score = float(1.0 / float(wordsInLabel))
            # We've seen this product before, so increment its hit count
            if product["productID"] in productHits:
                productHits[product["productID"]] += score
            else:
                productHits.update({product["productID"] : score})

    # Sort the product hits based on hitscore and cap the number of product results
    sortedProducts = sorted(productHits.items(), key=lambda x : x[1], reverse=True)
    sortedProducts = capNumberOfResults(sortedProducts, 10)
    detailList = convertToDetailList(sortedProducts, ingredient)
    return detailList


def capNumberOfResults(sortedProducts, limit):
    return sortedProducts[:limit]


# Turns the sortedProduct Dictionary into a list of lists that contains all properties of the product 
# Eact item in the list refers to a specific product for that ingredient. Each sublist contains detailed
# information about that product. Takes in the general recipe_ingredient entry as second parameter to evaluate portion cost
def convertToDetailList(sortedProducts, ingredient):
    productList = []
    for item in sortedProducts:
        productOverview = server.get_product_overview_db(item[0])

        standardizedUnit1 = ingredientManager.findKeyFromMeasureDict(productOverview["unit"])
        gramMeasure1 = convertAmountToGram(productOverview["quantity"], standardizedUnit1)
        standardizedUnit2 = ingredient["measure"]
        gramMeasure2 = convertAmountToGram(ingredient["quantity"], ingredient["measure"])
    
        portionCost = 0
        if productOverview["unit"] == "unit" and ingredient["measure"] == "unit":
            portionCost = float(productOverview["cost"]) * float(ingredient["quantity"])
        elif productOverview["unit"] == "unit" or ingredient["measure"] == "unit":
            portionCost = float(productOverview["cost"])
        else:
            portionCost = (gramMeasure2 / gramMeasure1) * float(productOverview["cost"])

        productDict = {"productID" : item[0], "hitScore" : item[1], "label" : productOverview["label"], "quantity" : productOverview["quantity"], "unit" : standardizedUnit1, "cost" : productOverview["cost"], "grams" : gramMeasure1, "portionCost" : portionCost, "image" : productOverview["imagelink"]}
        productList.append(productDict)
    return productList


# Converts the given quantity and unit to grams, etc. 5 pounds = x grams
def convertAmountToGram(quantity, unit):
    return float(quantity) *  unitConverter[str(unit)]

