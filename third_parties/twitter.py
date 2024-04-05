import os
from time import sleep

from dotenv import load_dotenv
from requests import options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def scrape_twitter_profile(twitter_profile_username: str):
    load_dotenv()

    """scrape information from Twitter profiles,
    Manually scape the information from the Twitter profile"""

    options = Options()

    #options.add_argument('--headless')
    options.add_argument('user-data-dir=twitter')

    driver = webdriver.Chrome(options=options)

    email = os.getenv("EMAIL") or ''
    password = os.getenv("PASS") or ''

    driver.get("https://www.twitter.com/login")

    delay = 15
    wait = WebDriverWait(driver, delay)

    try:
        wait.until(lambda driver: driver.find_element(by="css selector", value="input[autocomplete=username]"))
    except:
        pass

    driver.find_element(by="css selector", value="input[autocomplete=username]").send_keys(email)

    driver.find_elements(by="css selector", value="div[role=button]")[3].click()

    try:
        wait.until(lambda driver: driver.find_element(by="css selector", value="input[name=password]"))
    except:
        pass

    driver.find_element(by="css selector", value="input[name=password]").send_keys(password)

    driver.find_elements(by="css selector", value="div[role=button]")[3].click()

    sleep(2)

    driver.get(f"https://www.twitter.com/{twitter_profile_username}")

    print(driver.page_source)


if __name__ == "__main__":
    scrape_twitter_profile("dragaoazuljr")
