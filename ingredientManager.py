# Takes in a String for one ingredient such as
# "10 g of honey" And places into parameters
# Amount: 10, Measure: g, Item: honey

unitDictionary = {
    'cup': ["cup", "cups"],
    'tablespoon': ["tablespoon", "tblsp", "tbsps", "tbp", "tbps", "tbsp", "tablespoons"],
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
    'liter' : ["liter", "litre", "liters", "litres"],
    'unit' : ["unit", "box", "bag"]
}


def findKeyFromMeasureDict(measure):
    for key, value in unitDictionary.items():
        for term in value:
            if term == measure:
                return key
    return -1


def convertIngredient(ingredientString):
    ingredientString = filterInput(ingredientString)
    parameters = []

    # First we look for a measure substring. The reason for this is that the number/quantity is usually to the left of this
    # And it's easier than looking for a number when an ingredient specifies more than one way to measure
    measure = "unit"
    for word in ingredientString.split(" "):
        if findKeyFromMeasureDict(word) != -1:
            measure = findKeyFromMeasureDict(word)
            break

    # To find the amount we assume that it is the first value in the ingredientString
    # Collect numbers until we run unto an alphabetic character
    amount = ''
    indexOfMeasure = ingredientString.find(measure)
    if indexOfMeasure != -1:
        wordsBeforeMeasure = ingredientString[:indexOfMeasure].split(" ")
        for word in reversed(wordsBeforeMeasure):
            if not word.isalpha():
                amount = word + " " + amount
            else:
                break
    else:
        amount = '1'
        for word in ingredientString.split(" "):
            if not word.isalpha():
                amount = word
                break     

    item = ''
    if indexOfMeasure != -1:
        wordsAfterMeasure = ingredientString[indexOfMeasure:].split(" ")
        for word in wordsAfterMeasure[1:]:
            if word.isalpha():
                item += word
    else:
        for word in ingredientString.split(" "):
            if word.isalpha():
                item += word

    print("Work in Progress! Amount: " + amount + ". Measure: " + measure + ". Item: " + item)
    # For the text we filter out common words such as "of", "a", "dash", "store", "bought" etc.
    return parameters


def filterInput(string):
    filtered = ''
    for c in string:
        if c not in ["'", ",", '"', "(", ")", "-", "."]:
            filtered += c
        elif c == ",":
            filtered += "."
        else:
            filtered += " "
    return filtered


    
