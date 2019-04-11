from scrapy import Spider
import json

SEARCH_URL="https://turo.com/search?country=US&defaultZoomLevel=13&endDate=02%2F23%2F2019&endTime=08%3A00&international=true&isMapSearch=false&itemsPerPage=200&latitude=41.9772983&location=O%27Hare%2C%20Chicago%2C%20IL%2C%20USA&locationType=ZIP&longitude=-87.8368909&maximumDistanceInMiles=30&region=IL&sortType=RELEVANCE&startDate=02%2F19%2F2019&startTime=10%3A00&type=10"

class EdxSpider(Spider):
    name = "turo"
    allowed_domains =["turo.com","https://www.turo.com"]
    start_urls = (
        SEARCH_URL,
        )

    def parse(self, response):
        data = json.loads(response.body_as_unicode)
        print(data)
        print("FIRST KEYS:",data.keys())
        data = data[u'objects'][u'results']
        print("SECOND KEYS:",data[0].keys())
        return


