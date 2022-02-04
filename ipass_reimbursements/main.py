from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import choice
from bs4 import BeautifulSoup as bs
import os


import time
import datetime
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from random import choice
import logging


#add generic log file location and name
logging.basicConfig(filename='ipass.log', filemode="w", level=logging.INFO,format='%(asctime)s %(message)s')
    #Logging usage example:
    #logging.debug("This is a debug message")
    #logging.info("Informational message")
    #logging.error("An error has happened!")
logging.info("Job started")

def web_driver_set():
    ua_list = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36"
    ]

    dcap = dict(DesiredCapabilities.CHROME, javascriptEnabled=True)
    dcap["chrome.page.settings.resourceTimeout"] = 15
    dcap["chrome.page.settings.loadImages"] = True
    dcap["chrome.page.settings.userAgent"] = choice(ua_list)

    # instantiate a chrome options object so you can set the size and headless preference
    chrome_options = Options()
    # chrome_options.add_argument('headless')   # causing detection, access denied.
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery");
    chrome_options.add_argument("--start-maximized")

    # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
    # current directory
    print(os.getcwd())
    chrome_driver = os.getcwd() + "/chromedriver"
    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver, desired_capabilities=dcap)
    driver.delete_all_cookies()

    return driver

driver = web_driver_set()

def login(driver):
    url = "https://turo.com/us/en/login"
    driver.get(url)
    driver.implicitly_wait(2)
    try:
        # driver.find_element_by_xpath('//input[@id="email"]').send_keys('boltunoff@yahoo.com')
        # driver.find_element_by_xpath('//*[@id="pageContainer-content"]/div[1]/form/div[1]/input').send_keys('BLA')
        # login_form = driver.find_element_by_xpath('//*[@id="pageContainer-content"]/div[2]/div[1]/div/div/div/div/div[1]')
        # # email_form = driver.find_element_by_class_name('iframeFormGroup')
        # email_form = driver.find_element_by_class_name('emailLoginForm')
        # email_frame = driver.find_element_by_class_name('managedIframe-wrapper')
        # emailLoginForm = driver.find_element_by_class_name('emailLoginForm')

        # iFrame: its a separate html document within the main html. Need to swithch to iFrame context and find element within.
        driver.switch_to.frame(0)
        # TODO: add config for email and password
        driver.find_element_by_xpath("//input[@type='email']").send_keys('boltunoff@yahoo.com')
        driver.find_element_by_xpath("//input[@type='password']").send_keys('Dip765')
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.switch_to.parent_frame()

        driver.implicitly_wait(3)
        driver.save_screenshot('logged_in.png')

        #TODO:
        # 1. create new function to download the file: from line 87 onwards
        # 2. create test to read the file and process to SQLite, so not using loging often
        # 3. add proxies for driver funcion

        # Now since loggedin, changing URL to earnings
        earn_url = 'https://turo.com/us/en/earnings'
        driver.get(earn_url)

        # Click Download CSV button
        driver.find_element_by_xpath("//*[@href='/earnings/csv']").click()

        # CSV file downloads to Downloads folder automatically with name: earnings_export_20210826.csv
        from pathlib import Path
        downloads_path = str(Path.home() / "Downloads")
        todays_date = datetime.datetime.today().strftime('%Y%m%d')
        file_name = f'earnings_export_{todays_date}.csv'

        # with open(downloads_path + '/' + file_name, 'r') as f:
        #     print(f.readlines())

        import csv, sqlite3
        con = sqlite3.connect('turo.db')
        cur = con.cursor()
        import pandas
        df = pandas.read_csv(downloads_path + '/' + file_name)
        df['file_date'] = datetime.datetime.today()
        df["Vehicle ID"] = df["Vehicle ID"].fillna(0).astype(int)
        # if_exists='replace' - trunc and reloads table
        df.to_sql('raw_turo_transactions', con, if_exists='replace', index=False)



        con.commit()
        con.close()

    except Exception as e:
        driver.save_screenshot('error.png')
        raise

    # //*[@id="container"]/form

    # data = driver.page_source
    # soup = bs(data, "html.parser")
    # email = soup.find_all("input", class_="email")

    driver.save_screenshot('email_entered.png')

    # driver.implicitly_wait(3)
    # time.sleep(5)
    #     #enter text into search box for locatoin:
    # driver.find_element_by_xpath('//*[@id="pageContainer-content"]/div[1]/div[1]/div[2]/form/div[1]/input[1]').send_keys(city)
    # driver.implicitly_wait(3)       #also search by Chicago keyword, more cars available
    # time.sleep(5)
    #     #click search button in Ohare for a week ahead
    # try:
    #     driver.find_element_by_xpath('//*[@id="pageContainer-content"]/div[1]/div[1]/div[2]/form/div[4]/button').click()
    #     driver.implicitly_wait(3)
    #     time.sleep(5)
    # except Exception as e:
    #     driver.save_screenshot('button.png')
    #     raise

    url_now = driver.current_url  # URL for Current week search
    print(url_now)
    return url_now

login(driver)