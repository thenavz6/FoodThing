# Amount is usually given in grams of millileters

# List of unit of measures that coles uses
# It is important to put shorter terms like "g" after "kg" since first hit is taken
colesUnits = ["mg", "kg", "g", "ml", "l"]


with open("coles_products.txt") as f:
    content = f.readlines()

content = [x.strip().lower() for x in content] 

for entry in content:
    tmp = entry.split(",")
    name = tmp[0]
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

    # Find the quantity of the amount
    quantity = ''
    for char in measure:
        if not char.isalpha():
            quantity += char
        else:
            break
    
    if quantity.strip() == '':
        quantity = "1"


    # Find the unit of measure of the amount
    unit = "Unit"
    for value in colesUnits:
        if value in measure:
            unit = value
            break

    print("NAME: " + name, ". MEASURE: " + measure + ". COST: " + cost + ". LINK: " + link)
    print("QUANTITY: " + quantity + ". UNIT: " + unit)
    keywords = []
    for word in name.split():
        keywords.append(word)
    print("KEYWORDS: ")
    for word in keywords:
        print(word)

    # Write this into a database with two tables
    
    
    
    
