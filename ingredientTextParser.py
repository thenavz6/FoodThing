# Takes in a String for one ingredient such as
# 10 g of honey
# And places into parameters
# Amount: 10
# Measure: g
# Text: honey

measureUnits = ["cup", "tablespoon", "teaspoon", "oz", "g", "mg", "kg", "dash", "pinch", "pound", "ounce", "pint", "quart", "gallon", "milliliter", "millilitre", "liter", "litre" ]

def convertIngredient(ingredientString):
    parameters = []
    
    # To find the amount we assume that it is the first value in the ingredientString
    
    # Then we look for a given measure from our pre-kept 'dictionary' of possible measures
        # Make sure to account for plurals as well

    # For the text we filter out common words such as "of", "a", "dash", "store", "bought" etc.
    return parameters

