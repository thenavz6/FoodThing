#!/usr/bin/env python
# -*- coding: utf-8 -*- 

####################################################
# Takes in a String for one ingredient such as
# "10 to 15 g of honey" And places into parameters
# Amount: 15, Measure: g, Item: honey
###################################################

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


# Return the matching key if that's key's list has the given measure
def findKeyFromMeasureDict(measure):
    for key, value in unitDictionary.items():
        for term in value:
            if term == measure:
                return key
    return -1


# ingredientString is the user provided ingredient string which is then converted to necessary parameters such as 
# measure, amount and item
def convertIngredient(ingredientString):
    ingredientString = filterInput(ingredientString)   
    ingredientString = removeBracketedText(ingredientString)
    ingredientString = removeCommonWords(ingredientString)      
    parameters = []


    # First we look for a measure substring. The reason for this is that the number/quantity is usually to the left of this
    # And it's easier than looking for a number when an ingredient specifies more than one way to measure
    # If we cannot find a measure, we assume it is a "unit" such as an entire product etc. "5 oranges"
    measure = 'unit'
    givenMeasure = ''
    for word in ingredientString.split(" "):
        if findKeyFromMeasureDict(word) != -1:
            measure = findKeyFromMeasureDict(word)
            givenMeasure = word
            break


    # To find the amount we assume that it is somewhere to the left of where the units were written
    # Collect numbers to the left of the units given until we run unto an alphabetic character
    # This can still give us problems for instance if a range of numbers or strange text is given such as "1/2". Need to parse, so we do
    amount = ''
    if measure != 'unit':
        indexOfMeasure = (ingredientString.split(" ")).index(givenMeasure)
        wordsBeforeMeasure = (ingredientString.split(" "))[:indexOfMeasure]
        for word in reversed(wordsBeforeMeasure):
            if not word.isalpha() and len(amount) != 0:
                amount = word + " " + amount
            elif not word.isalpha():
                amount = word
            else:
                break
    else:
        for word in ingredientString.split(" "):
            if not word.isalpha():
                amount = word
                break     
    if amount == '':
        amount = '1'


    # Try and determine the actual product name or product keywords from the ingredientString
    item = ''
    if measure != 'unit':
        indexOfMeasure = (ingredientString.split(" ")).index(givenMeasure)
        wordsAfterMeasure = (ingredientString.split(" "))[indexOfMeasure:]
        for word in wordsAfterMeasure[1:]:
            if word.isalpha():
                item += word + " "
    else:
        for word in ingredientString.split(" "):
            if word.isalpha():
                item += word + " "


    print("Work in Progress! Amount: " + str(determineFinalAmount(amount)) + ". Measure: " + measure + ". Item: " + item)
    # print("Final amount is: " + determineFinalAmount(fractionStringToFloat(parseUnicodeFraction(amount))))
    # For the text we filter out common words such as "of", "a", "dash", "store", "bought" etc.
    return parameters


#################################################################
################### General Text Parser #########################
#################################################################

# Words that are alphabetic but don't describe the actual ingredients' product
# Also best to remove adjectives that are being used to describe cooking steps
commonWords = [
    "of", "the", "and", "or", "into", "&", "like", "some", "this", "that", "where", "when", "i", "to", "room", "temperature", "washed", "trimmed", 
    "large", "lg", "small", "sml", "taste", "tasted", "fine", "finely", "grated", "chopped", "torn", "cut", "pieces", "coaresly", "cooled", "melted",
    "then", "at", "thinly", "sliced", "diced", "medium"
]

# General input string filtering to remove unwanted characters and replace them with a space
def filterInput(string):
    filtered = ''
    for c in string:
        if c == u"⁄":
            filtered += "/"
        elif c in ["'", ",", '"', "-", "."]:
            filtered += " "
        else:
            filtered += c
    return filtered


# If there is any bracketed text (like this) in a string, it will be removed
def removeBracketedText(string):
    try:
        start, end = string.index("("), string.index(")")
        if (start > end):
            return string
        result = string[start:end+1]
        return string.split(result)[0] + string.split(result)[1]
    except ValueError:
        return string


# Removes any common words as contained in the commonWords list from this string
def removeCommonWords(string):
    result = ''
    for word in string.split():
        if word in commonWords:
            pass
        else:
            result += word + " "
    return result


#################################################################
############# Ingredient Measure Parser #########################
#===============================================================#
# Some useful conversions / common parsing that will be needed.
#################################################################

unicodeFractions = {
    u"⅒": 0.1,  
    u"⅑": 0.11111111,  
    u"⅛": 0.125, 
    u"⅐": 0.14285714, 
    u"⅙": 0.16666667, 
    u"⅕": 0.2, 
    u"¼": 0.25, 
    u"⅓": 0.33333333,  
    u"⅜": 0.375, 
    u"⅖": 0.4,  
    u"½": 0.5, 
    u"⅗": 0.6,
    u"⅝": 0.625,
    u"⅔": 0.66666667, 
    u"¾": 0.75, 
    u"⅘": 0.8, 
    u"⅚": 0.83333333, 
    u"⅞": 0.875, 
}

# If the given text is a unicode fraction then we convert it to an actual float we can use
def parseUnicodeFraction(text):
    # Check if any character in given value is a unicode fraction string
    result = ''
    for char in text:
        added = 0
        for key, value in unicodeFractions.items():
            if key == char:
                result += " " + str(value)
                added = 1
        if added == 0:
            result += char
    return result


# If the input word (only one word) describes any fraction then we return the float value it represents else we return the string
def fractionStringToFloat(word):
    if "/" in word:
        high, low = word.split("/")
        return str(float(int(high)/int(low)))
    return word


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

