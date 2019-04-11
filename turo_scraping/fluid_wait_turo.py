from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

from bs4 import BeautifulSoup
import time
import datetime
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import choice

def driver_set():
    ua_list = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36"
    ]

    dcap = dict(DesiredCapabilities.PHANTOMJS, javascriptEnabled=True)
    dcap["phantomjs.page.settings.resourceTimeout"] = 15
    dcap["phantomjs.page.settings.loadImages"] = True
    dcap["phantomjs.page.settings.userAgent"] = choice(ua_list)

    driver = webdriver.PhantomJS(desired_capabilities=dcap)  # PhantomJs should be in the same dir of python.py file within project
    driver.set_window_size(1920,1080)
    return driver

browser = driver_set()
# Load some webpage

url = "https://turo.com/search?country=US&defaultZoomLevel=13&endDate=02%2F23%2F2019&endTime=08%3A00&international=true&isMapSearch=false&itemsPerPage=200&latitude=41.9772983&location=O%27Hare%2C%20Chicago%2C%20IL%2C%20USA&locationType=ZIP&longitude=-87.8368909&maximumDistanceInMiles=30&region=IL&sortType=RELEVANCE&startDate=02%2F19%2F2019&startTime=10%3A00&type=10"
browser.get(url)
print(browser.title)

time.sleep(5)

# lastHeight = browser.execute_script("return document.body.scrollHeight")
# print(lastHeight)
# i = 0
# browser.get_screenshot_as_file("test03_1_"+str(i)+".png")
# while True:
# 	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# 	time.sleep(3)
# 	newHeight = browser.execute_script("return document.body.scrollHeight")
# 	print(newHeight)
# 	if newHeight == lastHeight:
# 		break
# 	lastHeight = newHeight
# 	i += 1
# 	browser.get_screenshot_as_file("test03_1_"+str(i)+".png")
#
# browser.quit()


#### Fluent Wait (setting up the wait like below), didn't work
wait = WebDriverWait(browser, 15, poll_frequency=2, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])

try:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pageContainer-content"]/div[4]/div/div[1]/div/div[1]/div/div/div[1]/div/div[1]/div/div/a')))
except Exception as e:
    browser.save_screenshot('search.png')
try:
    element = browser.find_element_by_xpath('//*[@id="pageContainer-content"]/div[4]/div/div[1]/div/div[1]/div/div/div[1]/div/div[1]/div/div/a').click()
except Exception as e:
    browser.save_screenshot('search2.png')
#veh_card_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pageContainer-content"]/div[4]/div/div[1]/div/div[1]/div/div/div[1]/div/div[1]/div/div/a')))
print(element)


