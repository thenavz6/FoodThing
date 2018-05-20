import product_db
import textParser

#############################################
### COLES specific scraped data parsing ####
#############################################

# List of unit of measures that coles uses
# It is important to put shorter terms like "g" after "kg" since first hit is taken
woolworthsUnits = ["mg", "kg", "g", "ml", "l"]

with open("recipething_scraped/woolworths_products.txt") as f:
    content = f.readlines()

content = [x.strip() for x in content] 

for entry in content:
    tmp = entry.split(",")
    length = len(tmp)
    name = tmp[0].lower()
    # Woolworths puts the name in the first field and then multiple (changing) amount of fields for possible keywords (maybe we can make use of these but not doing atm)
    # So the link is actually the last entry and price is the 2nd last.
    measure = ''
    for word in tmp[length - 3].split():
        if not word.isalpha():
            measure += word.lower()
    cost = tmp[length - 2].lower()
    link = tmp[length - 1]

    # Note that we need to extract quantity and unit of measure from the amount value
    # etc. 5g we need to extract the quantity = 5, unit = grams

    # Woolworths writes "5 pack" or "5pk" just like Coles
    # However, after the unit measure there is sometimes a gram 
    # measure. We will prefer the unit measure.

    # Try look for "pk"
    quantity = ''
    unit = ''
    try:
        foundIndex = name.index("pk")
        counter = 1
        number = ''
        while name[foundIndex - counter].isdigit():
            number += str(name[foundIndex - counter])
            counter += 1
        quantity = number[::-1]
        unit = "unit"
    except ValueError:
                pass

    # If we didn't find "pk" start looking for actual measures from woolworthsUnits
    if quantity.strip() == '':
        for term in woolworthsUnits:
            if term in measure:
                foundIndex = measure.index(term)
                counter = 1
                number = ''
                while measure[foundIndex - counter].isdigit():
                    number += str(measure[foundIndex - counter])
                    counter += 1
                quantity = number[::-1]
                unit = term
                break

    # Else we haven't found a "pk" or an appropriate unit measure
    if quantity.strip() == '':
        # Pick the first number and assume unit measure
        for word in measure.split():
            if word.isdigit():
                quantity = word
                unit = "unit"
   

    # If we still can't figure out quantity or got a non-number quantity, just guess 1
    if not quantity.strip().isdigit():
        quantity = "1"
        unit = "unit"
    quantity = str(quantity.strip())
            

    # Remove any common words or brand names from the products keywords to help better identify actual ingredient hits
    # Save the original name for the overview product TABLE
    originalName = name
    name = textParser.removeCommonWords(name)
    name = textParser.removeBrandWords(name)

    # Remove 's' or 'es' from the end of keywords. This should give better results.
    # When compared, ingredients in ProductManager.py will also remove 's' or 'es'. 
    keywords = []
    for word in name.split():
        if word.isalpha():
            if len(word) > 3:
                if word.endswith('es'):
                    word = word[:-2]
                elif word.endswith('s'):
                    word = word[:-1]
            keywords.append(word)

    # Remove duplicate words so a product called "Creams cream" doesn't hit twice. 
    keywords = list(set(keywords))

    # Write this into a database overview as well as keywords 
    product_db.add_product_overview(originalName, link, quantity, unit, cost, "woolworths")
    productId = product_db.find_product_id(originalName, link, cost)
    for word in keywords:
        product_db.add_product_keyword(productId, word)

