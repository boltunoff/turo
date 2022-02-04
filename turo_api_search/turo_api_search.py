# Found at:  https://stackoverflow.com/questions/54593816/scraping-through-python-selenium-or-beautifulsoup

# https://turo.com/search?airportCode=EWR&customDelivery=true&defaultZoomLevel=11&endDate=04%2F05%2F2019&endTime=11%3A00&international=true&isMapSearch=false&itemsPerPage=200&location=EWR&locationType=Airport&maximumDistanceInMiles=30&sortType=RELEVANCE&startDate=03%2F05%2F2019&startTime=10%3A00
# Working search URL:
# https://turo.com/us/en/search?country=US&defaultZoomLevel=11&delivery=false&endDate=02%2F08%2F2022&endTime=10%3A00&isMapSearch=false&itemsPerPage=200&latitude=37.7749295&location=San%20Francisco%2C%20CA&locationType=City&longitude=-122.41941550000001&region=CA&sortType=RELEVANCE&startDate=02%2F05%2F2022&startTime=10%3A00&useDefaultMaximumDistance=true
import requests
from pandas.io.json import json_normalize

base_url = 'https://turo.com'

url = 'https://turo.com/api/search?'

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.9',
'Connection': 'keep-alive',
'Host': 'turo.com',
'Referer': 'https://turo.com/us/en/search'}

# https://turo.com/us/en/search?airportCode=ORD&defaultZoomLevel=11&delivery=true&deliveryLocationType=airport&endDate=08%2F13%2F2021&endTime=10%3A00&international=true&isMapSearch=false&itemsPerPage=200&location=ORD%20%E2%80%94%20Chicago%20O%E2%80%99Hare%20International%20Airport%2C%20Chicago%2C%20IL&locationType=Airport&maximumDistanceInMiles=30&sortType=RELEVANCE&startDate=08%2F10%2F2021&startTime=10%3A00

# need two sets of parameters for Airport code search and for city
# params for airportCode:
params = {
'airportCode': 'ORD',
'customDelivery': 'true',
'defaultZoomLevel': '11',
'endDate': '09/07/2021',
'endTime': '11:00',
'international': 'true',
'isMapSearch': 'false',
'itemsPerPage': '200',
'location': "",
'locationType': 'Airport',
'maximumDistanceInMiles': '30',
'sortType': 'RELEVANCE',
'startDate': '09/04/2021',
'startTime': '10:00',
'type': '1'
}

# additional params
# 'type': '1'    # all random
# type=9 # SUVs
# type=10 #Minivans  ...
# 'type': '11' Trucks
# 'type': '8' Vans and Trucks

response = requests.get(url, headers=headers, params=params)
data = response.text(encoding='utf8')
# data = response.json()

print(data)
print(type(data))

search_id = data['searchId']
print(search_id)

for ele in data['list']:
    link = ele['vehicle']['url']
    print(base_url + link)




links_list = [ base_url + ele['vehicle']['url'] for ele in data['list'] ]

print(links_list)
print(len(links_list))