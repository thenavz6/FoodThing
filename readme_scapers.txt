README for recipething_scrapers

product_db.py defines the database tables and contains basic database execution commands.
Running this will initialise the database, creating the tables if they do not exist.

Each shop-specific-script-parser such as parseColes_add_db.py should import product_db.py.
In importing, the database is ensured to be initialised. 
Then the job of each shop-specific-parser is to take the scraped data and put it into sensible
format and then use the database execution functions located in product_db.py in order to store
the scraped data into the database.

Each scraper such as coles_scraper.py will actually scrape a shop's website and retrieve important
data and store it in a .txt file. The format of this file does not necessarily matter as it is the job
of that shops text parser to ensure consistency before storing it in the database. 
