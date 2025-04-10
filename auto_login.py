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
    browser.add_cookie({"name": "MUSIC_U", "value": "004B1E6BB712C73F40F707555DEE79ED84A389BAAA5084C6AC75281E283F2A15A0FB6002D18B66CB50784EAA3B02409F9CE8B564DDCECF72EA79DCEC8DB3B7D1850FE7011A69986D4B3D71AEB8DE243121BCF34DC2996005F3CAA5B71690EB40B2C28BE8CED9CA885E3109B2E7D3146E3AE54524DFBF8F2C83E14FDE10778B2A32033D3E73395775E1BC7F982ED1EC307A045F9317640056BF11F983F7147AF7DA5BB43B9EAAF30B7620E4294F1023829E5E61703479B180E3D40D67769EFDD3511637DE6FDC8E9BE35CA3B770A5CB74EC8717F43D445F6E0B25CC5AAE85A4CDB4B74B7DA132EBC9E2876859787DAF947413E1CC3445D3C4512C3AFDEA3F62225AC1DF6BF4402817D37FF4FE84A0547641B19923A1D26080C19B23B09CC741026E4F0086C84C4BFAE9ABEE0E0426003CE47214E6D23CB95F68D00E5FD0DB835EE83E325D40335A7CBC1FB18E740CA8F648CE87A407F0F5B378291542213B9380CF"})
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
