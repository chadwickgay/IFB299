


import requests 

from bs4 import BeautifulSoup

url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=ChIJ70tS1ZJZkWsR9Dnb1Gm82s0&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw"
response = requests.get(url)
file = response.json()

#cleanfile = BeautifulSoup(raw_html)

  #print (file)

#extract information
name = file['result']['name']
address = file['result']['formatted_address']
phone = file['result']['formatted_phone_number']
ratings = file['result']['rating']
website = file['result']['website']
price = file['result']['price_level']


#Storing Opening Hours

opening=[]
i=0
for i in range(len(file['result']['opening_hours']['weekday_text'])):
  opening.append(file['result']['opening_hours']['weekday_text'][i])

# Need to clean URLS
photos=[]
reference=[]
i=0
for i in range(len(file['result']['photos'])):
  photo =file['result']['photos'][i]
  photos.append(photo['html_attributions'][0])
  reference.append(photo['photo_reference'])
  

  #Review information need to clean review text
  Reviewername=[]
  reviewRating=[]
  reviewText=[]
  for i in range(len(file['result']['reviews'])):
    review=file['result']['reviews'][i]
    Reviewername.append(review['author_name'])
    reviewRating.append(review['rating'])
    reviewText.append(review['text'])
  

print (name, address, phone, opening, ratings, website, price, photos, reference, Reviewername, reviewRating, reviewText)