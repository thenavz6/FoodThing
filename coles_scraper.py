import sys, re, time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

catagories = ["bread-bakery/fresh","bread-bakery/packaged-bread-bakery","fruit-vegetables/boxes-fruit-vege","fruit-vegetables/fruit","fruit-vegetables/vegetables","fruit-vegetables/salad-herbs","fruit-vegetables/nuts-dried-fruit","meat-seafood-deli/fresh-meat","meat-seafood-deli/seafood","meat-seafood-deli/deli-meats","meat-seafood-deli/deli-specialty","dairy--eggs-meals/milk-3796063","dairy--eggs-meals/fresh-eggs-534560","dairy--eggs-meals/cheese-3885551","dairy--eggs-meals/dairy-eggs","dairy--eggs-meals/fresh-pasta-sauces","dairy--eggs-meals/garlic-bread-pastry-sheets","dairy--eggs-meals/ready-to-eat-meals","dairy--eggs-meals/smallgoods","dairy--eggs-meals/meat-alternatives","pantry/breakfast","pantry/snacks","pantry/confectionery","pantry/herbs-spices","pantry/health-foods","pantry/stocks-gravy","pantry/baking","pantry/jams--honey-spreads","pantry/condiments","pantry/sauces","pantry/oils-vinegars","pantry/pasta--rice--grains","pantry/canned-foods--soups-noodles","pantry/coffee-3116064","pantry/pantry-tea","pantry/local-foods","frozen/baby-toddler-meals","frozen/frozen-chips-wedges","frozen/convenience-meals","frozen/frozen-desserts","frozen/frozen-fish-seafood","frozen/frozen-fruit","frozen/ice-cream-frozen-yoghurt","frozen/frozen-meat","frozen/frozen-party-food-pastries","frozen/frozen-pizzas","frozen/frozen-vegetables","frozen/ice","drinks/soft-drinks-3314551","drinks/cordials","drinks/water-3314673","drinks/juice-3314585","drinks/sports-drinks-iced-tea","drinks/flavoured-milk-3314681","drinks/tea-drinks","drinks/coffee-drinks-3314631","drinks/long-life-milk-3314687","drinks/non-alcoholic-3314656","liquor/beer-cider","liquor/red-fortified-wines","liquor/white-wines","liquor/spirits","liquor/premixed-non-alcoholic","liquor/ice-accessories","international-food/cuisine","international-food/kosher-foods","international-food/halal-foods","healthy-living/gluten-free","healthy-living/organic","healthy-living/healthier-choices","healthy-living/diet-sports-nutrition","healthy-living/vegetarian","healthy-living/vitamins-health-supplements"]
urlLeft = "https://shop.coles.com.au/online/a-national/"
urlRight = "?tabType=everything&tabId=everything&personaliseSort=false&orderBy=20601_6&errorView=AjaxActionErrorResponse&requesttype=ajax&beginIndex="

ingredientListRegex = "\"products\":.*?\"searchInfo"
fieldFormat = "p1\":{\"o\".*?\"t\".*?,"
#price, weight, name, image link
extractFormat = "o\":\"(\d+\.\d+)\".*?\"O3\":\[\"(.*?)\".*?\"s\":\"(.*?)\",\"t\":\"(.*?)\","
#gets number of pages
#numPages = int(input("how many pages should be searched? "))

ingredients = {}    
outputFile = input("output to what file? ")
failed = []

#gets the ingredients
time.clock()
for catagory in catagories:
	print("\n\n"+catagory+"\n")
	i = 0
	n = 0
	tries = 5
	next = True
	while next:
		url = urlLeft + catagory + urlRight + str(n)
		#print(url+"\n\n\n")
		retry = True
		while retry:
			try:
				t = time.clock()
				r = Request(url)
				page = str(urlopen(r).read())
				retry = False
				
			except HTTPError:
				while time.clock() - t < 3:pass # This makes the program wait 3 seconds between requests 
				if tries > 0:
					retry = True
					tries -=1
				else:
					retry = False
					failed.append(catagory)
				print("Error: resending " + str(i))
		#print("-----\n\n")
		#print(page)
		#print("\n\n\n-----")
		ingredientsList = re.search(ingredientListRegex,page).group(0)
		ingr = re.findall(fieldFormat, ingredientsList)
		#print(ingr)
		if len(ingr) > 0:
			n += len(ingr)
			for ing in ingr:
				data = re.search(extractFormat,ing)
				if data != None and data.group(3) not in ingredients:
					ingredients[data.group(3)] = (data.group(2),float(data.group(1)),"https://shop.coles.com.au"+data.group(4))
				#ingredients.append((data.group(3),data.group(2),float(data.group(1)),"https://shop.coles.com.au"+data.group(4)))
			while time.clock() - t < 0.5:pass # This makes the program wait half a second between requests
		else:
			next = False
			
		print("recieved page " + str(i+1))
		i = i+1
    


#ingredients
with open(outputFile,'w') as f:
    for i in ingredients.keys():
        f.write(re.sub("-"," ",i)+", "+ingredients[i][0]+", "+str(ingredients[i][1])+",     "+ingredients[i][2]+"\n")
        
print("Done! written results to " + outputFile)
if len(failed) > 0:
	print("\n\nFailed sections:\n")
	for fail in failed:
		print(fail+"\n")
