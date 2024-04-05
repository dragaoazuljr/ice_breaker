from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

def get_profile_url(name: str) -> str:
    options = Options()

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.google.com")

    search_box = driver.find_element(by="css selector", value="textarea[name='q']")

    search_box.send_keys(f"{name} LinkedIn")

    search_box.submit()

    delay = 15
    wait = WebDriverWait(driver, delay)

    try:
        wait.until(lambda driver: driver.find_element(by="id", value="search"))
    except:
        pass
    
    list_of_a = driver.find_elements(by="css selector", value="#search a")

    result = ''

    for item in list_of_a:
        name = item.find_element(by="css selector", value="h3").text
        link = item.get_attribute("href")

        if link:
            result = link
            break

    return result

