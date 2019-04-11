# Found at:  https://stackoverflow.com/questions/54593816/scraping-through-python-selenium-or-beautifulsoup

# https://turo.com/search?airportCode=EWR&customDelivery=true&defaultZoomLevel=11&endDate=04%2F05%2F2019&endTime=11%3A00&international=true&isMapSearch=false&itemsPerPage=200&location=EWR&locationType=Airport&maximumDistanceInMiles=30&sortType=RELEVANCE&startDate=03%2F05%2F2019&startTime=10%3A00

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
'Referer': 'https://turo.com/search'}


# need two sets of parameters for Airport code search and for city
# params for airportCode:
params = {
'airportCode': 'ORD',
'customDelivery': 'true',
'defaultZoomLevel': '11',
'endDate': '04/17/2019',
'endTime': '11:00',
'international': 'true',
'isMapSearch': 'false',
'itemsPerPage': '200',
'location': "",
'locationType': 'Airport',
'maximumDistanceInMiles': '30',
'sortType': 'RELEVANCE',
'startDate': '04/15/2019',
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
data = response.json()

print(data)
search_id = data['searchId']
print (search_id)

for ele in data['list']:
    link = ele['vehicle']['url']
    print (base_url + link)




links_list = [ base_url + ele['vehicle']['url'] for ele in data['list'] ]

print(links_list)
print(len(links_list))