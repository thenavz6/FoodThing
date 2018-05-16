import product_db
import textParser

#############################################
### COLES specific scraped data parsing ####
#############################################

# List of unit of measures that coles uses
# It is important to put shorter terms like "g" after "kg" since first hit is taken
colesUnits = ["mg", "kg", "g", "ml", "l"]

with open("coles_products.txt") as f:
    content = f.readlines()

content = [x.strip().lower() for x in content] 

for entry in content:
    tmp = entry.split(",")
    name = textParser.removeCommonWords(tmp[0])
    measure = tmp[1]
    cost = tmp[2]
    link = tmp[3]

    # Note that we need to extract quantity and unit of measure from the amount value
    # etc. 5g we need to extract the quantity = 5, unit = grams

    # Get rid of the approx. which Coles places sometimes before the measure
    # They write this differently sometimes
    try:
        measure = measure.split("approx.")[1].strip()
    except IndexError:
        pass
    try:
        measure = measure.split("approx")[1].strip()
    except IndexError:
        pass 

    # Find the quantity of the amount. Coles always writes this first.
    quantity = ''
    for char in measure.strip():
        if not char.isalpha():
            quantity += char
        else:
            break
    if quantity.strip() == '':
        quantity = "1"

    # Find the unit of measure of the amount
    # Use the colesUnits list to find a unit Coles uses
    unit = "unit"
    for value in colesUnits:
        if value in measure:
            unit = value
            break

    # Remove 's' or 'es' from the end of keywords. This should give better results.
    # When compared, ingredients in ProductManager.py will also remove 's' or 'es'.
    keywords = []
    for word in name.split():
        if len(word) > 3:
            if word.endswith('es'):
                word = word[:-2]
            elif word.endswith('s'):
                word = word[:-1]
        keywords.append(word)

    # Write this into a database with two tables    
    product_db.add_product_overview(name, link, quantity, unit, cost, "coles")
    productId = product_db.find_product_id(name)
    for word in keywords:
        product_db.add_product_keyword(productId, word)

