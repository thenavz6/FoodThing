from textParser import *

###
# Takes care of converting ingredient strings such as:
# "About 2 to 2 1/2 (approx.) tbps of brown sugar"
# Into understandable format such:
# Quantity: 2.5, Measure: Tablespoons, Item: brown sugar
# This is so that we can compare sensible data 
# to products to determine costs and other such things
###

unitDictionary = {
    'cup': ["cup", "cups"],
    'tablespoon': ["tablespoon", "tblsp", "tbsps", "tbp","tbs", "tbps", "tbsp", "tablespoons"],
    'teaspoon': ["teaspoon", "teasp", "teasps", "tsp", "tsps", "teaspoons"],
    'ounce' : ["oz", "ounce", "ounces"],
    'gram' : ["gram", "grams", "g"],
    'milligram' : ["milligram", "milligrams", "mg"],
    'kilogram' : ["kilogram", "kilograms", "kg"],
    'dash' : ["dash", "dashes"],
    'pinch' : ["pinch", "pinches"],
    'pound' : ["pound", "pounds", "lb"], 
    'pint' : ["pint", "pints"],
    'quart' : ["quart", "quarts"],
    'gallon' : ["gallon", "gallons"],
    'milliliter' : ["milliliter", "millilitre", "milliliters", "millilitres", "ml"],
    'liter' : ["liter", "litre", "liters", "litres", "l"],
    'unit' : ["unit", "box", "bag", "container", "bunch"]
}


# Return the matching key if that's key's list has the given measure
def findKeyFromMeasureDict(measure):
    for key, value in unitDictionary.items():
        for term in value:
            if term == measure:
                return key
    return -1



# The 'main' function of the ingredientManager
# ingredientString is the user provided ingredient string which is then converted to necessary parameters  
# such as: measure, amount and item
def convertIngredient(ingredientString):
    ingredientString = filterInput(ingredientString)   
    ingredientString = removeBracketedText(ingredientString)
    ingredientString = removeCommonWords(ingredientString) 
    ingredientString = ingredientString.lower()     
    parameters = ["", "", ""]


    # First we look for a measure substring. The reason for this is that the number/quantity is usually to the left of this
    # And it's easier than looking for a number when an ingredient specifies more than one way to measure
    # If we cannot find a measure, we assume it is a "unit" such as an entire product etc. "5 oranges"
    measure = 'unit'
    givenMeasure = ''
    for word in ingredientString.split():
        if findKeyFromMeasureDict(word) != -1:
            measure = findKeyFromMeasureDict(word)
            givenMeasure = word
            break


    # To find the amount we assume that it is somewhere to the left of where the units were written
    # Collect numbers to the left of the units given until we run unto an alphabetic character
    # This can still give us problems for instance if a range of numbers or strange text is given such as "1/2". Need to parse, so we do
    amount = ''
    if measure != 'unit':
        indexOfMeasure = (ingredientString.split()).index(givenMeasure)
        wordsBeforeMeasure = (ingredientString.split())[:indexOfMeasure]
        for word in reversed(wordsBeforeMeasure):
            if not word.isalpha() and len(amount) != 0:
                amount = word + " " + amount
            elif not word.isalpha():
                amount = word
            else:
                break

    else:
        for word in ingredientString.split():
            if not word.isalpha():
                amount = word
                break     
    if amount == '':
        amount = '1'


    print(amount)

    # Try and determine the actual product name or product keywords from the ingredientString
    item = ''
    if measure != 'unit':
        indexOfMeasure = (ingredientString.split()).index(givenMeasure)
        wordsAfterMeasure = (ingredientString.split())[indexOfMeasure:]
        for word in wordsAfterMeasure[1:]:
            if word.isalpha():
                item += word + " "
    else:
        for word in ingredientString.split():
            if word.isalpha():
                item += word + " "
    item = item.lower()
    item = item.strip()

    # print("[DEBUG] Amount: " + str(determineFinalAmount(amount)) + ". Measure: " + measure + ". Item: " + item)
    # For the text we filter out common words such as "of", "a", "dash", "store", "bought" etc.
    parameters[0] = str(determineFinalAmount(amount))
    parameters[1] = measure
    parameters[2] = item
    return parameters



# We have to consider multipe things when try to determine the actual quantity needed such as certain characters used to describe
# fractions, given a range of quantities etc.
def determineFinalAmount(string):
    # Get rid of all unicode and replace them with floats
    string = parseUnicodeFraction(string)
    value = []
    finalAmount = 0.0

    # Go through each number that we have and convert any "2/5" fraction strings to floats
    # Note that this value list is stored backwards, so later mentioned values can be deemed more significant
    for word in string.split():
        try:
            value.insert(0, (float(fractionStringToFloat(word))))
        except ValueError:
            value.insert(0, 0)

    # Go backwards through all values and pick the highest integer and any < 1 fractions to the right of it
    for num in value:
        if int(num) - float(num) == 0:
            finalAmount = finalAmount + float(num)
            break
        elif finalAmount == 0.0:
            finalAmount += float(num)
        else:
            break     

    # If we tried our best and still can't get anything, assume quantity is 1
    if finalAmount == 0.0:
        finalAmount = 1.0

    return finalAmount

