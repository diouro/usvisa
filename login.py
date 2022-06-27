import time
import random
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = 'deliopimenta@hotmail.com'
PASSWORD = '10302011'
COUNTRY_CODE = 'en-br'  # en-ca for Canada-English
SCHEDULE = '39739222'

URL = f"/{COUNTRY_CODE}/niv/schedule/{SCHEDULE}/appointment"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def login():
    # Bypass reCAPTCHA
    driver.get(f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv")
    time.sleep(1)
    a = driver.find_element(By.XPATH, value='//a[@class="down-arrow bounce"]')
    a.click()
    time.sleep(1)

    href = driver.find_element(By.XPATH, value='//*[@id="header"]/nav/div[2]/div[1]/ul/li[3]/a')
    href.click()
    time.sleep(1)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "commit")))

    a = driver.find_element(By.XPATH, value='//a[@class="down-arrow bounce"]')
    a.click()
    time.sleep(1)

    do_login_action()
    do_process_reschedule()

def do_login_action():
    user = driver.find_element(By.ID, value='user_email')
    user.send_keys(USERNAME)
    time.sleep(random.randint(1, 2))

    pw = driver.find_element(By.ID, value='user_password')
    pw.send_keys(PASSWORD) 
    time.sleep(random.randint(1, 2))

    box = driver.find_element(By.CLASS_NAME, value='icheckbox')
    box .click()
    time.sleep(random.randint(1, 2))

    btn = driver.find_element(By.NAME, value='commit')
    btn.click()
    time.sleep(random.randint(1, 2))

    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Continue')]")))
    except TimeoutError:
        login()

def do_process_reschedule():
    btnContinue = driver.find_element(By.LINK_TEXT, value='Continue')
    btnContinue.click()
    time.sleep(1)

    rescheduleExpand = driver.find_element(By.LINK_TEXT, value='Reschedule Appointment')
    rescheduleExpand.click()
    time.sleep(1)

    btnReschedule = driver.find_element(By.XPATH, value='//a[@href="'+URL+'"]')
    btnReschedule.click()
    time.sleep(1)

    btnRescheduleContinue = driver.find_element(By.NAME, value='commit')
    btnRescheduleContinue.click()
    time.sleep(random.randint(1, 2))

    
if __name__ == "__main__":
    login()