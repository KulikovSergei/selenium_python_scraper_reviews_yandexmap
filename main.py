import time

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
#from selenium.common.exceptions import WebDriverException

from modules import get_reviews_from_YandexMaps
from modules import scroll_to_bottom

browser = webdriver.Firefox()
action = webdriver.ActionChains(browser)

url_links = 'url_links.txt'

def main(browser, action, url_links):

    with open(url_links, 'r') as file:
        urls = [url.rstrip('\n') for url in file]
    
    for url in urls:
        browser.get(url)
        time.sleep(1)
        browser.implicitly_wait(5)

        #browser.find_element(By.CSS_SELECTOR, '._name_reviews').click()
        #time.sleep(3)

        scroll_to_bottom(driver = browser, action=action)

        content = browser.page_source

        soup = BeautifulSoup(content, features='html.parser')
        data = get_reviews_from_YandexMaps(bs4_soup=soup)
        title = soup.find('h1', class_='card-title-view__title').get_text()

        #print(data.head(5))
        data.to_excel('{}_reviews.xlsx'.format(title))
    
    browser.quit()  # remove this line to leave the browser open

if __name__ == '__main__':
    main(browser=browser, action=action, url_links=url_links)
    print('Work is DONE!')