#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#################################################################
#################  General Text Parser #########################
#################################################################

# Words that are alphabetic but don't describe the actual ingredients' product
# Also best to remove adjectives that are being used to describe cooking steps
# Put in lower case only.
commonWords = [
    "of", "the", "and", "or", "into", "&", "like", "some", "this", "that", "where", "when", "i", "to", "room", "temperature", "washed", "trimmed", "garden",
    "large", "lg", "small", "sml", "taste", "tasted", "fine", "finely", "grated", "chopped", "torn", "cut", "pieces", "coaresly", "cooled", "melted",
    "then", "at", "thinly", "sliced", "diced", "medium", "container", "store", "bought", "such", "as", "before", "after", "pkt", "coarsely", "lightly",
    "beaten", "for", "more", "plus", "pans", "fresh", "whites", "sifted", "pan", "peeled", "cuts", "drained", "slices", "cans", "cool", "warm", "chunks", "frozen", "pack", 
    "brand", "cold", "hot", "all", "purpose", "hulled", "whole", "branded", "tasty", "farm", "caged", "cage", "range", "red", "green", "food", "plain", "reduced", 
    "salted", "unsalted", "ready", "light", "mixed", "natural", "spring", "ultimate", "traditional", "organic", "normal", "size", "sized", "very", "free", "table", "plain",
    "jumbo", "eco", "living", "x", "x-large", "extra", "pure", "cook", "cooking", "pure", "clear", "clean", "squeezed", "loose", "packed", "prepacked", "gourmet",
    "essence", "pieces", "sticks", "bars", "blocks", "flavoured", "flavoured", "instant", "fat", "skim", "lite", "full", "baby", "only", "minced", "australia",
    "australian", "gluten", "quick", "double", "single", "triple", "tempting", "tempt", "texting", "spraying", "nonstick", "dairy"
]

# If we can know what words in an ingredient or product describe a brand then 
# we can make the searches have better hits. Put in lower-case only.
brandNames = [
    "coles", "beechworth", "manning", "valley", "capilano", "saxa", "hoyts", "masterfoods", "cadbury", "arnott's", "kellog's",
    "mckenzies", "continental", "queens", "heinz", "obento", "balconi", "evian", "mount", "franklin", "kraft", "nestle", "nescafe",
    "lidnt", "sanitarium", "golden", "circle", "bega", "spc", "uncle", "tobys", "streets", "john", "west", "farmers", "pura",
    "kewpie", "norganic", "praise", "thomy", "crosse", "hellmans", "nobbys", "csr", "jeenys", "wings", "pace", "queen", "twinings",
    "betty", "crocker", "aunt", "a2", "devondale", "pauls", "tempo", "creative"
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


# Remove a certain character from input and replace it with a space
def filterCharacter(string, char):
    filtered = ''
    for c in string:
        if c == char:
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
        if word.lower() in commonWords:
            pass
        else:
            result += word + " "
    return result


# Removes any brand names/words as contained in the brands List from this string
def removeBrandWords(string):
    result = ''
    for word in string.split():
        if word.lower() in brandNames:
            pass
        else:
            result += word + " "
    return result


# Turns a string such as "12ml" into something like "12 ml"
def seperateAlphaAndDigit(string):
    result = ''
    lastIsDigit = False
    for c in string:
        if lastIsDigit and c.isalpha():
            result += ' '
            result += c
        else:
            if c.isdigit():
                lastIsDigit = True
            else:
                lastIsDigit = False
            result += c
        if c.isalpha():
            lastIsDigit = False
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

