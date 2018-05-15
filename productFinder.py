# Given a single ingredient string with fields: quantity, unit, item
# will attempt to find best matches from the product database and also
# calculate cost/proportions etc.

import server

# Parameter: The keywords for a given ingredient etc. "Fat free milk"
# For each word in the keyword (which has been parsed) we look for products
# that contain this keyword. The product then has its score incremented 
# depending on how long the label of the product is and hence relevence
def findBestProducts(keywords):
    # Dictionary that stores how many hits a given product has. etc 'product12' : 5, 'product2' : 2
    productHits = {}

    # For each keyword etc. 'sour cream buttermilk' we want to search the product database
    for word in keywords.split():
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
    return sortedProducts


def capNumberOfResults(sortedProducts, limit):
    return sortedProducts[:limit]


# Turns the sortedProduct Dictionary into a list that contains all properties of the product 
# for example [[id, label, cost, price, unit], [id, label, cost, price, unit]]
def convertToDetailList(sortedProducts):
    productList = []
    for item in sortedProducts:
        productOverview = server.get_product_overview_db(item[0])
        productDict = {"productID" : item[0], "hitScore" : item[1], "label" : productOverview["label"], "quantity" : productOverview["quantity"], "unit" : productOverview["unit"], "cost" : productOverview["cost"]}
        productList.append(productDict)
    return productList

