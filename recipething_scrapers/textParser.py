#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#################################################################
#################  General Text Parser #########################
#################################################################

# Words that are alphabetic but don't describe the actual ingredients' product
# Also best to remove adjectives that are being used to describe cooking steps
commonWords = [
    "of", "the", "and", "or", "into", "&", "like", "some", "this", "that", "where", "when", "i", "to", "room", "temperature", "washed", "trimmed", 
    "large", "lg", "small", "sml", "taste", "tasted", "fine", "finely", "grated", "chopped", "torn", "cut", "pieces", "coaresly", "cooled", "melted",
    "then", "at", "thinly", "sliced", "diced", "medium", "container", "store", "bought", "such", "as", "before", "after", "pkt", "coarsely", "lightly",
    "beaten", "for", "more", "plus", "pans", "fresh", "whites", "sifted", "pan", "peeled", "cut", "drained", "slices", "cans", "cool", "warm", "chunks", "frozen", "pack", "brand",
    "cold", "hot", "all", "purpose", "hulled", "whole", "coles", "Coles", "branded",
    "red", "green"
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
############# Ingredient Measure Parser ########################
#===============================================================
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

