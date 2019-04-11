import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs

url = "https://turo.com/search?country=US&defaultZoomLevel=13&endDate=02%2F23%2F2019&endTime=08%3A00&international=true&isMapSearch=false&itemsPerPage=200&latitude=41.9772983&location=O%27Hare%2C%20Chicago%2C%20IL%2C%20USA&locationType=ZIP&longitude=-87.8368909&maximumDistanceInMiles=30&region=IL&sortType=RELEVANCE&startDate=02%2F19%2F2019&startTime=10%3A00&type=10"

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--start-maximized")

# what are other options available for chrome... like desired capabilities  ?
# https://www.programcreek.com/python/example/100025/selenium.webdriver.ChromeOptions
# http://chromedriver.chromium.org/capabilities

search_result_list = []

def collect_results(browser):
    data = browser.page_source
    soup = bs(data, "html.parser")
    try:
        search_result = soup.find_all('div', {'class': "searchResult"})
        search_result_list.append(search_result)
    except Exception as e:
        print(str(e))
        raise


browser = webdriver.Chrome(chrome_options=options,executable_path='C:\\Users\\Dzmitry\\PycharmProjects\\todo-api\\chromedriver.exe')
browser.get(url)
# zoom out to have max listings on the page
#browser.execute_script("document.body.style.zoom='25%'")
time.sleep(5)
collect_results(browser)
browser.save_screenshot('1main.png')

# scroll for this number of pixels:
#browser.execute_script("window.scrollBy(0,600)")

lenOfPage = browser.execute_script(
    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

lenOfPage
print(lenOfPage)
browser.save_screenshot('2main.png')

# Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
match = False
count = 1
while (match == False):
    lastCount = lenOfPage
    time.sleep(5)
    count =+1
    lenOfPage = browser.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    collect_results(browser)
    browser.save_screenshot('3main_{count}.png'.format(count=count))
    if lastCount == lenOfPage:
        match = True

browser.save_screenshot('4main.png')

print(len(search_result_list))
for i in search_result_list:
    print(i)




# only finds last two car listings...
    # may need to save objects.. links for cars as scrolling happening ... or...
# search_result = soup.find_all('div', {'class': "searchResult"})

#





