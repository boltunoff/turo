
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
import bs4 as bs
import urllib.request
import time

class Client(QWebPage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        time.sleep(5)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def on_page_load(self):
        self.app.quit()

url = "https://turo.com/search?country=US&defaultZoomLevel=13&endDate=02%2F23%2F2019&endTime=08%3A00&international=true&isMapSearch=false&itemsPerPage=200&latitude=41.9772983&location=O%27Hare%2C%20Chicago%2C%20IL%2C%20USA&locationType=ZIP&longitude=-87.8368909&maximumDistanceInMiles=30&region=IL&sortType=RELEVANCE&startDate=02%2F19%2F2019&startTime=10%3A00&type=10"
client_response = Client(url)
source = client_response.mainFrame().toHtml()
soup = bs.BeautifulSoup(source,'lxml')

#els = soup.find_all('a', class_= 'vehicleCard')
els = soup.find("div", {"id": "pageContainer-content"})
print(els)
print(type(els))
for e in els:
    print(e)

# #pageContainer-content > div:nth-child(4) > div > div.searchResultsGrid > div > div.schumacherGrid > div > div > div.ReactVirtualized__Grid > div > div:nth-child(1) > div > div > a
#pageContainer-content > div:nth-child(4) > div > div.searchResultsGrid > div > div.schumacherGrid > div > div > div.ReactVirtualized__Grid > div > div:nth-child(1) > div > div > a


