import os
from time import sleep

from dotenv import load_dotenv
from requests import options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def scrape_twitter_profile(twitter_profile_url: str):
    load_dotenv()

    """scrape information from Twitter profiles,
    Manually scape the information from the Twitter profile"""

    options = Options()

    options.add_argument('--headless')
    options.add_argument('user-data-dir=twitter')

    driver = webdriver.Chrome(options=options)

    email = os.getenv("EMAIL") or ''
    password = os.getenv("PASS") or ''
    username = os.getenv("TWITTER_USERNAME") or ''

    driver.get("https://www.twitter.com/login")

    sleep(1)

    current_url = driver.current_url

    delay = 15
    wait = WebDriverWait(driver, delay)

    if current_url.find("login") != -1:
        try:
            wait.until(lambda driver: driver.find_element(by="css selector", value="input[autocomplete=username]"))
        except:
            pass

        driver.find_element(by="css selector", value="input[autocomplete=username]").send_keys(email)
        driver.find_elements(by="css selector", value="div[role=button]")[3].click()

        sleep(1)

        try:
            driver.find_element(by="css selector", value="input[name=text]").send_keys(username)
            driver.find_elements(by="css selector", value="div[role=button]")[1].click()

            sleep(2)
        except:
            pass

        driver.find_element(by="css selector", value="input[name=password]").send_keys(password)
        driver.find_elements(by="css selector", value="div[role=button]")[2].click()

    sleep(1)

    driver.get(twitter_profile_url)

    try:
        wait.until(lambda driver: driver.find_element(by="css selector", value="div[data-testid=tweetText]"))
    except:
        pass

    tweets_div = driver.find_elements(by="css selector", value="div[data-testid=tweetText]")

    tweets = [tweet.text for tweet in tweets_div]

    driver.execute_script("window.scrollTo(0, 1000);")

    sleep(1)

    tweets_div = driver.find_elements(by="css selector", value="div[data-testid=tweetText]")

    # add more tweets to the list excluding the ones already added
    tweets += [tweet.text for tweet in tweets_div if tweet.text not in tweets]

    # return string of tweets
    return ", ".join(tweets)
