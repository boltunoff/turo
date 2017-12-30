from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
from random import choice
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os.path
import logging

#add generic log file location and name
logging.basicConfig(filename='turotask_minivans.log', filemode="w", level=logging.INFO,format='%(asctime)s %(message)s')
    #Logging usage example:
    #logging.debug("This is a debug message")
    #logging.info("Informational message")
    #logging.error("An error has happened!")
logging.info("Job started")

def driver_set():
    ua_list = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36"
    ]

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.resourceTimeout"] = 15
    dcap["phantomjs.page.settings.loadImages"] = False
    dcap["phantomjs.page.settings.userAgent"] = choice(ua_list)

    driver = webdriver.PhantomJS(desired_capabilities=dcap)  # PhantomJs should be in the same dir of python.py file within project
    driver.set_window_size(1920,1080)
    return driver

driver = driver_set()

# car_types: SUVS, MINIVANS, CARS.
# to search only for regular cars, excluding suvs and minivans, need to apply filter on web page, instead of just
# specifying url with /cars...
# add url and html objects for /cars only search results

def navigate_to_base_url(car_type, city):
    url = "https://turo.com/rentals/%s/" % car_type
    driver.get(url)
    driver.implicitly_wait(3)
    time.sleep(5)
        #click input search form:
    driver.find_element_by_xpath('//*[@id="pageContainer-content"]/div[1]/div[1]/div[2]/form/div[1]/input[1]').click()
    driver.implicitly_wait(3)
    time.sleep(5)
        #enter text into search box for locatoin:
    driver.find_element_by_xpath('//*[@id="pageContainer-content"]/div[1]/div[1]/div[2]/form/div[1]/input[1]').send_keys(city)
    driver.implicitly_wait(3)       #also search by Chicago keyword, more cars available
    time.sleep(5)
        #click search button in Ohare for a week ahead
    try:
        driver.find_element_by_xpath('//*[@id="pageContainer-content"]/div[1]/div[1]/div[2]/form/div[4]/button').click()
        driver.implicitly_wait(3)
        time.sleep(5)
    except Exception, e:
        driver.save_screenshot('button.png')

    driver.implicitly_wait(3)
    time.sleep(5)
    url_now = driver.current_url  # URL for Current week search
    print url_now
    return url_now
    # parse current URL to find current search dates and update search dates for weeks ahead and for 3 days search
    # update current URL with new start/end dates +7 days; +3 days
                #all_cars[0].prettify()
#https://turo.com/search?type=10&location=Chicago%2C%20IL%2C%20USA&country=US&region=IL&locationType=City&models=&makes=&fromYear=0&startDate=06%2F27%2F2017&startTime=10%3A00&endDate=07%2F04%2F2017&endTime=10%3A00&category=ALL&instantBook=false&customDelivery=false&maximumDistanceInMiles=30&sortType=RELEVANCE&isMapSearch=false&latitude=41.8781136&longitude=-87.6297982&defaultZoomLevel=11

#TODO: consider user input as: Type of Car(minivan, suv, **regular), City, Start Date and End Date.
# ??? use above url as a base having user inputs as a parameters...?

url_now = navigate_to_base_url('minivans', 'Chicago')

logging.info("Cleaning and parsing dates from URL")

def cln_dates(url_now):
    url_lst = url_now.split("&")
    for s in url_lst:
        if 'startDate' in s:
            startDate = s
        elif 'endDate' in s:
            endDate = s

    start_list = startDate.split('=')
    start_date_str = start_list[1].replace("2F", "-").split("%")
    start_dt = "".join(start_date_str)

    end_list = endDate.split('=')
    end_date_str = end_list[1].replace("2F", "-").split("%")
    end_dt = "".join(end_date_str)
    return start_dt, end_dt
        #(u'06-12-2017', u'06-19-2017')  strings
        #TODO convert to date formate and add 7 or 3 days and create new url with them
        #startDate=05%2F11%2F2017        and      endDate=05%2F18%2F2017
        # a = u'06-27-2017'
        # a1 = datetime.datetime.strptime(a,"%m-%d-%Y")
        # a17 = a1 + datetime.timedelta(days=7)
        # a17s = datetime.datetime.strftime(a17,"%m-%d-%Y")

def parse_data():   # add argument url_now
    #driver = driver_set()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #driver.close()
    #use the heirarchical nature of HTML structure to grab precisely the content that I am interested in
    # I will grab all of the elements that are within "li" tags and are also members of class "u-baseBottomMargin"
    all_cars = soup.find_all('li', {'class': 'u-baseBottomMargin'})

    #print "Example of the 1st element with text of HTML soup object:  \n", all_cars[0]
    #all_cars[0].span.get_text()

    hrefs_list = []         # parse link to find car ID
    car_id_list = []
    year_list = []
    make_list = []   # Make Model

    for i in all_cars:      # trying to combine all data elements in one loop and to add to dict
        hrefs_list.append(i.a["href"])
        href = i.a["href"]
        car_id = href.split("/")[6][:6]  # 6th element of the link, and 6th element of ID node /654321/
        car_id_list.append(car_id)
        year = i.span.get_text()
        year_list.append(i.span.get_text())
        model = i.p.get_text()
        make_list.append(i.p.get_text())

    prices = soup.find_all('p', {'class': 'vehicleWithDetails-value'}) # different element for pricess, couldn't get_text from all_cars
    price_list = []     # Prices
    for i in prices:
        price_list.append(i.get_text())

    logging.info("Prices conversion to floats started")
    price_list_fl = [float(e) for e in price_list] #convert unicode to floats

    #print "Minimum price for today: ", min(price_list_fl)
    #print "Maximum price for today: ", max(price_list_fl)
    #print "Average price for today: ", sum(price_list_fl)/float(len(price_list_fl))    #resolve unicode

    publn_dt = time.strftime("%m/%d/%Y %H:%M:%S")
    print "Search on: ", publn_dt

    logging.info("Found %d prices for the cars", len(price_list_fl))


    search_start_dt, search_end_dt = cln_dates(url_now)   #calling function to get dates

    data = {
        'search_start_dt': search_start_dt,
        'search_end_dt':search_end_dt,
        'publn_dt' : publn_dt,
        'links' : hrefs_list,
        'car_id' : car_id_list,
        "year" : year_list,
        'make' : make_list,
        'price' : price_list_fl
    }

    import pandas as pd

    df = pd.DataFrame(data)
    df = df[['car_id','links','year','make','price','search_start_dt','search_end_dt','publn_dt']]  #changing order of DF
    print df
    return df

fname = 'turo_minivans_data.csv'
import logging
# add filemode="w" to overwrite
#logging.basicConfig(filename="turo_parse3.log", filemode="w", level=logging.INFO)
#logging.debug("This is a debug message")
#logging.info("Informational message")
#logging.error("An error has happened!")
df = parse_data()

import os.path
logging.info("Writing data to CSV file... %s " % fname)
def write_file(df):
    try:
        if os.path.exists(fname):       #todo may need to check if the load for the same date exists?
            with open(fname, 'a') as f:
                df.to_csv(f, header=False, index=False)
                print(len(df), "records written to CSV file %s" % fname)
        else:
            with open(fname, 'a') as f:
                df.to_csv(f, header=True, index=False)
                print(len(df), "records written to CSV file %s" % fname)
    except IOError:
        logging.error("Can't open %s. Please check if the %s is now open" %(fname,fname))
        logging.info("Nothing is written to the file")

data = write_file(df)
print('Job is done for one iteration')

# calculating future dates from the url_now
s, e = cln_dates(url_now)
s_dt = datetime.datetime.strptime(s, "%m-%d-%Y") #convert to date format from string
e_dt_in6m = datetime.timedelta(days = 7 *26)   # start date in url in 6 months(26 weeks)

def timespan(s_dt, e_dt_in6m, delta=datetime.timedelta(days=7)): #returns dates for 6 months ahead
    curr_dt_plus7 = s_dt + datetime.timedelta(days = 7)     # first search date for a week ahead
    while curr_dt_plus7 < e_dt_in6m:
        yield curr_dt_plus7
        curr_dt_plus7 += delta

#for day in timespan(s_dt, e_dt_in6m, delta=datetime.timedelta(days=7)):
    #url_coll =
    # print day

def date_repl_url():
    for day in timespan(s_dt, e_dt_in6m, delta=datetime.timedelta(days=7)):
        url_coll = []
        s_dt_str = datetime.datetime.strftime(day, '%m-%d-%Y')
        s_dt_str_url = s_dt_str.replace('-', '%2F')

def future_url():
    # 1. add 7 days to start and end dt
    # 2. substitute dates in URL
    # 3. run all the rutine again.
        # convert Dates like this:
        # startDate=05%2F11%2F2017        and      endDate=05%2F18%2F2017
        # a = u'06-27-2017'
        # a1 = datetime.datetime.strptime(a,"%m-%d-%Y")
        # a17 = a1 + datetime.timedelta(days=7)
        # a17s = datetime.datetime.strftime(a17,"%m-%d-%Y")
    pass



# good example: https://github.com/fankcoder/findtrip/blob/master/findtrip/findtrip/spiders/spider_ctrip.py
# https://github.com/ianibo/SirsiDynixIBistroScraper/blob/master/scraper.py

#TODO: search on diff timelines: a week ahead, a month ahead, 6 months ahead
#TODO: when future dates function is ready, decouple main functions from iterations(each week, each car type, etc),
#  create logs for each iteration.


