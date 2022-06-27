import logging
import time
import json
import random
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = 'deliopimenta@hotmail.com'
PASSWORD = '10302011'
SCHEDULE = '39739222'
COUNTRY_CODE = 'en-br'  # en-ca for Canada-English
FACILITY_ID = '55'  # 94 for Toronto (others please use F12 to check)

MY_SCHEDULE_DATE = "2023-07-20"  # 2022-05-16 WARNING: DON'T CHOOSE DATE LATER THAN ACTUAL SCHEDULED
MY_CONDITION = lambda month, day: True  # MY_CONDITION = lambda month, day: int(month) == 11 and int(day) >= 5

SLEEP_TIME = 60   # recheck time interval

DATE_URL = f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/schedule/{SCHEDULE}/appointment/days/{FACILITY_ID}.json?appointments[expedite]=false"
TIME_URL = f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/schedule/{SCHEDULE}/appointment/times/{FACILITY_ID}.json?date=%s&appointments[expedite]=false"

APPOINTMENT_URL = f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/schedule/{SCHEDULE}/appointment"
EXIT = False

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
logging.basicConfig(level=logging.INFO, filename="visa.log", filemode="a+", format="%(asctime)-15s %(levelname)-8s %(message)s")


def login():
    # Bypass reCAPTCHA
    driver.get(f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv")
    time.sleep(1)
    a = driver.find_element(By.XPATH, value='//a[@class="down-arrow bounce"]')
    a.click()
    time.sleep(1)

    logging.info("start sign")
    href = driver.find_element(By.XPATH, value='//*[@id="header"]/nav/div[2]/div[1]/ul/li[3]/a')
    href.click()
    time.sleep(1)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "commit")))

    logging.info("click bounce")
    a = driver.find_element(By.XPATH, value='//a[@class="down-arrow bounce"]')
    a.click()
    time.sleep(1)

    do_login_action()


def do_login_action():
    logging.info("input email")
    user = driver.find_element(By.ID, value='user_email')
    user.send_keys(USERNAME)
    time.sleep(random.randint(1, 3))

    logging.info("input pwd")
    pw = driver.find_element(By.ID, value='user_password')
    pw.send_keys(PASSWORD) 
    time.sleep(random.randint(1, 3))

    logging.info("click privacy")
    box = driver.find_element(By.CLASS_NAME, value='icheckbox')
    box .click()
    time.sleep(random.randint(1, 3))

    logging.info("commit")
    btn = driver.find_element(By.NAME, value='commit')
    btn.click()
    time.sleep(random.randint(1, 3))

    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Continue')]")))
        logging.info("Login successfully!")
    except TimeoutError:
        logging.warning("Login failed!")
        login()


def get_date():
    driver.get(DATE_URL)
    if not is_logined():
        login()
        return get_date()
    else:
        content = driver.find_element(By.TAG_NAME, value='pre').text
        date = json.loads(content)
        return date


def get_time(date):
    time_url = TIME_URL % date
    logging.info("get_time")
    driver.get(time_url)
    content = driver.find_element(By.TAG_NAME, value='pre').text
    logging.info("content")
    data = json.loads(content)
    time = data.get("available_times")[-1]
    logging.info("Get time successfully!")
    return time


# BUGGY
def reschedule(date):
    global EXIT
    logging.info("Start Reschedule")

    availableTime = get_time(date)
    driver.get(APPOINTMENT_URL)

    # # NEW STEP:: confirm reschedule appointment
    logging.info("Confirm reschedule")
    btn = driver.find_element(By.NAME, value='commit')
    btn.click()
    time.sleep(random.randint(1, 3))


def is_logined():
    content = driver.page_source
    if(content.find("error") != -1):
        return False
    return True


def print_date(dates):
    for d in dates:
        logging.info("%s \t business_day: %s" %(d.get('date'), d.get('business_day')))
    logging.info("\n")


last_seen = None
def get_available_date(dates):
    global last_seen

    def is_earlier(date):
        return datetime.strptime(MY_SCHEDULE_DATE, "%Y-%m-%d") > datetime.strptime(date, "%Y-%m-%d")

    for d in dates:
        date = d.get('date')
        if is_earlier(date) and date != last_seen:
            _, month, day = date.split('-')
            if(MY_CONDITION(month, day)):
                last_seen = date
                return date


if __name__ == "__main__":
    login()
    retry_count = 0
    while 1:
        if retry_count > 6:
            break
        try:
            logging.info(datetime.today())

            dates = get_date()[:5]
            print_date(dates)
            date = get_available_date(dates)
            if date:
                reschedule(date)

            if(EXIT):
                break

            time.sleep(SLEEP_TIME)
        except:
            retry_count += 1
            time.sleep(60*5)
