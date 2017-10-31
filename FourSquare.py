import requests

placeName='ribs-and-rumps'
placeID = '4ef3e29ca69d3d38d5bd93a9'

def getPlaceID (placeName):
	url = 'https://api.foursquare.com/v2/venues/explore?client_id=02ZEPEK2153SCZD1VCAJKT5O1JQIDPD4CS2XC1N50I12LJSG&client_secret=0LXE02XDG0G4POGWBHNTBMQU5ZYIPSJHLCOEHKC2HWIHGECZ&ll=40.7,-74&v=20170926&m=foursquare&near=Brisbane,QLD&limit=1&query=' + placeName

	response = requests.get(url)
	file = response.json()

	placeID = file['response']['groups'][0]['items'][0]['venue']['id']

	return(placeID)
 
def location_information (placeName):

	placeID = getPlaceID(placeName)

	url2 = 'https://api.foursquare.com/v2/venues/' + placeID + '?client_id=02ZEPEK2153SCZD1VCAJKT5O1JQIDPD4CS2XC1N50I12LJSG&client_secret=0LXE02XDG0G4POGWBHNTBMQU5ZYIPSJHLCOEHKC2HWIHGECZ&v=20130815&v=20170927&m=foursquare'
	response2 = requests.get(url2)
	API = response2.json()
	# priceL = API['response']['venue']['price']['tier']
	priceM = API['response']['venue']['price']['message']
	category = API['response']['venue']['categories'][0]['name']
	
	itemName[]
	item
	for i in range(len(API['response']['venue']['attributes']['items'])):
		items = API['response']['venue']['attributes']['items'][i]
		item_information[i]= items['displayName']


	print(priceM, category)

location_information(placeName)