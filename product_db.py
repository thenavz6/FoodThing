import sqlite3
DATABASE = 'products.db'

#############################################
### General Product database Functions #####
#############################################

# General database functions
def add_product_overview(name, imagelink, quantity, unit, cost, store):
    db = sqlite3.connect(DATABASE) 
    cursor = db.cursor()
    cursor.execute('INSERT INTO product_overview (label, imagelink, quantity, unit, cost, store) VALUES ("'+name.lower()+'","'+imagelink+'","'+quantity+'","'+unit.lower()+'","'+cost+'","'+store.lower()+'");')  
    db.commit()
    db.close()
     

def add_product_keyword(productId, keyword):
    db = sqlite3.connect(DATABASE)
    db.execute('INSERT INTO product_keywords VALUES ('+(str(productId)).lower()+',"'+keyword.lower()+'");')
    db.commit()
    db.close()


# Sometimes the name can hit other products so we combine it with the imagelink and cost and hope (extremely likely) compound primary key
def find_product_id(name, imagelink, cost):
    entry = [name.lower(), imagelink, cost]
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM product_overview WHERE label=? AND imagelink=? AND cost=?', entry)
    productId = cursor.fetchone()[0]
    db.close()
    return productId

    
def init():
    db = sqlite3.connect(DATABASE)
    db.execute('CREATE TABLE IF NOT EXISTS product_overview (productID INTEGER PRIMARY KEY AUTOINCREMENT, label TEXT, imagelink TEXT, quantity TEXT, unit TEXT, cost TEXT, store TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS product_keywords (productID INTEGER, keyword TEXT, FOREIGN KEY (productID) REFERENCES product_overview(productID))')
    db.commit()
    db.close()

init()

