#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#################################################################
#################  General Text Parser #########################
#################################################################

# Words that are alphabetic but don't describe the actual ingredients' product
# Also best to remove adjectives that are being used to describe cooking steps
# Put in lower case only.
commonWords = [
'&', '100%', '99%', 'after', 'all', 'and', 'approved', 'as', 'at', 'australia', 'australian', 'baby', 'baked', 'bars', 'be', 'beaten', 'before', 'blocks', 'bottle', 
'bought', 'bowl', 'brand', 'branded', 'brown', 'cage', 'caged', 'cans', 'carb', 'certified', 'chopped', 'chunks', 'classic', 'clean', 'cleaned', 'clear', 'coaresly', 
'coarsely','cold', 'combo', 'container', 'cook', 'cooking', 'cool', 'cooled', 'crumbs', 'cut', 'cuts', 'dairy', 'deluxe', 'diced', 'double', 'drained', 'dried',
'eastern','eat','eco', 'essence', 'extra', 'farm', 'fat', 'fine', 'finely', 'finest', 'flavoured', 'flip', 'food', 'for', 'free', 'fresh', 'frozen', 'full', 'garden', 'gi', 
'gluten', 'go', 'gourmet', 'grated', 'grazing', 'green', 'heritage', 'hot', 'hulled', 'i', 'imported', 'instant', 'into', 'jar', 'jumbo', 'kid', 'kids', 'kit', 'la', 
'large', 'le', 'lean', 'lg', 'light', 'lightly', 'like', 'lite', 'living', 'loose', 'macro', 'market', 'medium', 'melted', 'microwavable', 'mild', 'minced', 'mini', 'mixed', 
'more', 'natural', 'naturally', 'nonstick', 'normal', 'northern', 'odd', 'of', 'off', 'on', 'only', 'or', 'organic', 'pack', 'packed', 'pan', 'pans', 'peeled', 
'petit','pieces', 'pkt', 'plain', 'plus', 'prefer', 'premium', 'prepacked', 'proactiv', 'produce', 'pure', 'purpose', 'quick', 'range', 'raw', 'ready', 'red', 'reduced', 
'removed', 'roast', 'roasted', 'room', 'salted', 'semi', 'shave', 'shaved', 'shred', 'shreds', 'sifted', 'single', 'size', 'sized', 'skim', 'sliced', 'slices', 'slow', 
'small', 'sml', 'so','some', 'southern', 'spraying', 'spring', 'squeezed', 'stem', 'sticks', 'store', 'style', 'such', 'table', 'taste', 'tasted', 'tasty', 'temperature', 
'tempt','tempting', 'texting', 'that', 'thawed', 'the', 'then', 'thin', 'thinly', 'this', 'to', 'torn', 'traditional', 'trim', 'trimmed', 'triple', 'ultimate', 'unsalted', 
'value','very', 'vintage', 'warm', 'washed', 'western', 'when', 'where', 'white', 'whites', 'whole', 'wood', 'x', 'x-large', 'you', 'yum', 'yummy']


# If we can know what words in an ingredient or product describe a brand then 
# we can make the searches have better hits. Put in lower-case only. Words should not possible identify an ingredient etc "Almond breeze" we only insert 'breeze'
brandNames = [
'&', '3', '9', 'a2', "abbott's", 'abc', "abe's", 'absolutely', 'adelaide', 'adriano', 'aeroplane', 'ainsley', 'al', 'alambra', "allen's", 'allens', 'allowrie', 'always', 
'am', 'ami', 'amoy', "amy's", 'anchor', 'angas', 'annalisa', 'anzac', 'ardomona', 'arkadia', 'arnolds', "arnott's", 'arnotts', 'ashgrove', 'asian', 'aunt', 'aussie', 
'australias', 'ayam', 'babies', 'babushkas', 'babybel', 'bakery', 'balconi', 'barilla', 'barrel', 'barrys', 'batchelors', 'bay', 'bazaar', 'beak', 'beechworth', 
'beerenberg', 'bega', 'bell', 'belle', 'belvita', 'bertocchi', 'bertolli', 'betty', "betty's", 'bhuja', "bickford's", 'bickfords', 'birch', 'birds', 'blue', 'bonne', 
'bonsoy', 'bonvallis', 'boost', 'breeze', 'brioche', 'brothers', 'bruema', 'brunswick', 'bsc', 'bud', 'buderim', 'bulla', 'burgen', 'bushells', 'butterfingers', 'byron', 
'cadbury', 'cakemark', 'calbee', 'calci', 'califia', 'calve', "campbell's", 'campbells', 'cape', 'capilano', "carman's", 'carnation', 'casa', 'cashel', 'castello', 
'castlemaine', 'cayen', 'caught', 'cecco', 'ceres', "chang's", 'changs', 'chef', 'chia', 'chobani', "chris'", 'ciabatta', 'circle', 'clarks', 'clearly', "cleaver's", 'co.', 'cobram', 
'coles', 'company', 'complete', 'connoisseur', 'continental', 'coon', 'cornwells', 'cortas', 'costi', 'country', 'coyo', 'created', 'creative', 'creek', 'crocker', 'crosse', 
'csr', 'cuisine', 'culture', "d'affinois", "d'orsogna", 'daffinois', 'daily', 'dairylea', 'daly', 'danone', 'dare', 'darrell', 'de', 'del', 'delfi', 'deli', 'delights', 
'devondale', 'diamond', 'dilmah', 'dodoni', 'dole', 'dollar', 'don', 'doree', 'dorsogna', 'dutch', 'earth', 'easiyo', 'edgell', 'envy', 'essentials', 'essnetials', 'estate', 
'evia', 'evian', 'eye', 'famiglia', 'family', 'fantastic', 'farm', 'farmers', 'farmhouse', 'favourites', 'five', 'five:am', 'flinders', 'flora', 'formaggio', 'foster', 
'fountain', 'four', 'fournee', 'france', 'franklin', 'freedom', 'frey', 'frico', 'fromager', 'fuji', 'galbani', 'game', 'garden', 'geoff', 'gippsland', 'gloaria', 'gold', 
'golden', 'gotzinger', 'goulburn', 'grasslands', 'gravox', 'greens', 'greenseas', 'grinders', 'gulley', 'gullon', 'ha', 'halo', 'hans', 'hansells', 'harriot', 'heagen', 
'heart', 'hedys', 'heilala', 'heinz', "helga's", 'helgas', 'hellenic', 'hellmans', 'hills', 'hillview', 'holland', 'home', 'homebrand', 'house', 'hoyts', 'hunter', 'huon', 
'igor', 'ile', 'imperial', 'ingham', "ingham's", 'inghams', 'island', 'jalna', 'jamie', 'jansz', 'jarlsberg', 'jazz', 'jeans', 'jeenys', 'john', 'just', 'kanzi', 
'karlsberg', 'kee', "kellog's", 'kellogs', 'kerrygold', 'kettle', 'kewpie', 'kikkoman', 'kinder', 'king', 'kipling', 'kirks', 'kitchen', 'kr', 'kraft', 'kum', 'la', 
'latina', 'lavazza', 'lawsons', 'lea', 'lee', 'leggo', "leggo's", 'leggos', 'lel', 'lemnos', 'leonardi', 'liberty', 'liddells', 'lidnt', 'lifesavers', 'lighthouse', 
'lipton', 'logue', 'love', 'low', 'lucia', 'lucky', 'lurpak', 'luv', 'm&m', 'macro', 'madagascan', 'magaret', 'maggi', 'maggie', 'maharajas', 'mainland', 'maman', 'mamma', 
'manning', 'marco', 'marino', 'masterfoods', 'maximum', 'mayfair', "mayver's", 'mazzetti', 'mccain', 'mccormick', 'mccormicks', 'mcdonnells', "mckenzie's", 'mckenzies', 
'meadowlea', 'meredith', 'miguel', 'mil', 'mills', 'mission', 'mocoona', 'moira', 'mon', 'monecatini', 'moreton', 'moro', 'mother', 'mount', 'mr', 'mrs', 'msa', 'multix', 
'mutti', 'nakula', 'nana', 'naturally', 'nature', "nature's", 'natvia', 'nescafe', 'nestle', 'newmans', 'nibbles', "nobby's", 'nobbys', 'norganic', 'normandie', 'nudie', 
'nutterlex', 'oak', 'ob', 'obela', 'obento', 'ocean', 'odysseus', 'one', 'own', 'pace', 'paesenella', 'pandaroo', 'paradise', 'paramount', 'park', 'pascall', 'passage', 
'pataks', 'paul', 'pauls', 'peckish', 'perfect', 'perfecto', 'peters', 'philadelphia', 'picasso', 'pitango', 'plumrose', 'polo', 'port', 'praise', 'president', 'primo', 
'pura', 'pure', 'purebred', 'pureharvest', 'queen', 'queens', 'red', 'remo', 'river', 'riverina', 'rock', 'rockit', 'rokeby', 'roma', 'roo', 'rspca', 'sakata', 'salamanca', 
'san', 'sanitarium', 'sara', 'sargents', 'saunders', 'saxa', 'schobs', "schwob's", 'sealord', 'select', 'servers', 'share', 'simmone', 'singetons', 'sister', 'smart', 
'smith', 'smokehouse', 'somderdale', 'sons', 'south', 'spc', 'spiral', 'steggles', 'streets', 'style', 'sunbeam', 'sunny', 'sunrice', 'sunsweet', 'super', 'superior', 
'table', 'tailor', 'talleys', 'tamar', 'tasmanian', 'tassal', 'tegel', 'tempo', 'tetley', 'thinkfood', 'thins', 'thomy', 'tibaldisignature', 'tip', "toby's", 'tobys', 
'tonight', 'top', 'toscano', 'traditional', 'trident', 'tuckers', 'twenty', 'twinings', 'twisted', 'uncle', 'unicorn', 'union', 'vaalia', 'valley', 'village', 'vitasoy', 
'vittoria', 'waite', 'wares', 'watchers', 'wattle', 'way', 'weight', 'well', 'west', 'wester', 'wicked', 'willow', 'wings', 'wokka', 'wonder', 'woolworths', 'yarra', 
'yoplait', "yumi's", 'yummis', 'zanetti', 'zoosh', 'zumbo', 'zuppa']

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

