import os
import pickle
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from bs4 import BeautifulSoup

def scrape_linkedin_profile(linkedin_profile_url: str):

    load_dotenv()

    """scrape information from LinkedIn profiles,
    Manually scape the information from the LinkedIn profile"""
 
    proxy = os.getenv("PROXY")

    options = Options()

    options.add_argument('--headless')
    options.add_argument('user-data-dir=linkedin')

    driver = webdriver.Chrome(options=options)

    email = os.getenv("EMAIL") or ''
    password = os.getenv("PASS") or ''

    driver.get("https://www.linkedin.com/login")

    time.sleep(1)

    current_url = driver.current_url

    if current_url.find("login") != -1:
        driver.find_element(by="id", value="username").send_keys(email)
        driver.find_element(by="id", value="password").send_keys(password)

        driver.find_element(by="css selector", value=".btn__primary--large.from__button--floating").click()

        time.sleep(20)

    driver.get(linkedin_profile_url)

    delay = 15
    wait = WebDriverWait(driver, delay)

    try:
        wait.until(lambda driver: driver.find_element(by="id", value="experience"))
    except:
        pass

    cookies = driver.get_cookies()

    pickle.dump(cookies, open("cookies-linkedin.pkl", "wb"))

    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser')

    name = soup.find("h1", class_="text-heading-xlarge inline t-24 v-align-middle break-words")
    title = soup.find("div", class_="text-body-medium break-words")
    location = soup.find("span", class_="text-body-small inline t-black--light break-words")
    about = soup.find("div", class_="pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center")
    experience = soup.find("ul", class_="pvs-list")

    if name:
        name = name.text.strip()
    if title:
        title = title.text.strip()
    if location:
        location = location.text.strip()
    if about:
        about = about.text.strip()
    if experience:
        experience = '\n'.join(list(dict.fromkeys(experience.stripped_strings)))

    driver.quit()

    # return {
    #     "name": name,
    #     "title": title,
    #     "location": location,
    #     "about": about,
    #     "experience": experience
    # }

    return f"""Name = {name}, Job Title = {title}, Location = {location}, About = {about}, Experience = {experience}"""
    
