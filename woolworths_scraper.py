import sys, re, time
#from urllib.parse import urlencode
#from urllib.request import Request, urlopen
#from urllib.error import HTTPError
import requests

catagories = [('1-E5BEE36E','fruit-veg','Fruit & Veg'),('1_D5A2236','meat-seafood-deli','Meat, Seafood & Deli'),('1_DEB537E','bakery','Bakery'),('1_6E4F4E4','dairy-eggs-fridge','Dairy, Eggs & Fridge'),('1_39FD49C','pantry','Pantry'),('1_ACA2FC2','freezer','Freezer'),('1_5AF3A0A','drinks','Drinks'),('1_C8BFD01','liquor','Liquor')]
url = "https://www.woolworths.com.au/apis/ui/browse/category"
reqData = {'categoryId':'','pageNumber':1,'pageSize':36,'sortType':'Name','url':'/shop/browse/','location':'/shop/browse/','formatObject':'{"name":""}'}
#{'categoryId':'1-5931EE89','pageNumber':1,'pageSize':36,'url':'/shop/browse/fruit-veg','location':'/shop/browse/fruit-veg','formatObject':'{"name":"Fruit & Veg"}'}
fieldFormat = "\"Price\":.*?LargeImageFile\":\".*?\""
#Price, Name, Description, Image link
extractFormat = "\"Price\":(\d*?\.?\d*?),.*?\"Name\":\"(.*?)\".*?\"Description\":\"(.*?)\".*?\"LargeImageFile\":\"(.*?)\""
#gets number of pages
#numPages = int(input("how many pages should be searched? "))

ingredients = {}    
outputFile = input("output to what file? ")
failed = []

#gets the ingredients
time.clock()
for catagory in catagories:
	print("\n\n"+catagory[2]+"\n")
	i = 1
	n = 0
	next = True
	while next:
		retry = True
		tries = 5
		while retry:
			try:
				t = time.clock()
				currReqData = reqData
				currReqData['categoryId'] = catagory[0]
				currReqData['pageNumber'] = i
				currReqData['url'] = '/shop/browse/'+catagory[1]
				currReqData['location'] = '/shop/browse/'+catagory[1]
				currReqData['formatObject'] = '{"name":"'+catagory[2]+'"}'
				
				page = requests.post(url,data=currReqData,timeout=5).text
				retry = False
				
			except:
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
		ingr = re.findall(fieldFormat, page)
		#print(ingr)
		if len(ingr) > 0:
			next = False
			for ing in ingr:
				data = re.search(extractFormat,ing)
				
				if data != None and re.sub("^\s*","",data.group(2)) not in ingredients:
					name = re.sub("^\s*","",data.group(2))
					ingredients[name] = (name,re.sub(".*>","",re.sub("^\s*?"+name+"\s*","",data.group(3))),float(data.group(1)),data.group(4))
					next = True
			while time.clock() - t < 0.5:pass # This makes the program wait half a second between requests
		else:
			next = False
		print("recieved page " + str(i))
		i = i+1
    


#ingredients
with open(outputFile,'w') as f:
    for i in ingredients.keys():
        f.write(ingredients[i][0]+", "+ingredients[i][1]+", "+str(ingredients[i][2])+", "+ingredients[i][3]+"\n")
        
print("Done! written results to " + outputFile)
if len(failed) > 0:
	print("\n\nFailed sections:\n")
	for fail in failed:
		print(fail[2]+"\n")
