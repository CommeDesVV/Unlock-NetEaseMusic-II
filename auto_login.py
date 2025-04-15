# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "008E23540BDFCDCD746B9E1451671BFDB25DCE2B93F7C0F345EB7DD7C96C44FF7F6206F8A8089D8398101F046670D670F9A31CA9046C8F0C8E987809F7D928906286B3EF5875D25C56D799E8E4CE0626AD88379A50511B322ED9B01314F14EE0F8FC56A7257D217D2A9BC7828196ED08B20E704AA6703F15DB0BD305DA5F9C74BA868BC1DCBEB718429910E728C8BAFEE46A95B30BBF58449F9AC656E2BF21F4D9CF4570BEE41C15238111C4A1AB95B5920AC817B596A100412E25CE5FBEA5779DF3357517EEF0BF3E37034B40FD01062B6C5DDE4894C54672DD495525CFE0DDEFAA6FDB538A8FC3D29B7F142F71788AEE14CC7B4D2A60065ECE31DC32D14232CD1C21A4D0A37967565D933FF489EC70367618AE062D3A3AD09A49D3FD6977CCF874369E1918F6C075590FF6E41359054D4CFF53C8774827D682A049BFE02DFB2B96D8149389CC6B51F5C049A38C155B5ECEB499711E9C44E82F44BF2B1C0BE5EF"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
