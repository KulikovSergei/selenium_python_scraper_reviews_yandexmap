from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time
import numpy as np
import pandas as pd


# scroll web element till the end
def scroll_to_bottom(driver, action):

    old_position = 0
    new_position = None

    site_body = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".scroll__container"))) 
    action.move_to_element(site_body).perform()

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script("return arguments[0].scrollHeight", site_body)
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', site_body)
        time.sleep(5)
        # Get new scroll position
        new_position = driver.execute_script("return arguments[0].scrollHeight", site_body)


# retrive all downloaded reviews
def get_reviews_from_YandexMaps(bs4_soup):

    reviews = []
    authors = []
    authors_status = []
    authors_ratings = []
    publication_date = []

    for result in bs4_soup.findAll('div', class_='business-reviews-card-view__review'):
        try:
            reviews.append(result.find('span', class_='business-review-view__body-text').get_text())
        except:
            reviews.append(np.NaN)

        try:
            authors.append(result.find('div', class_='business-review-view__author').\
                           find('span', attrs={'itemprop': 'name'}).get_text())
        except:
            authors.append(np.NaN)
            
        try:
            authors_status.append(result.find('div', class_='business-review-view__author').\
                                  find('div', class_='business-review-view__author-profession').get_text())
        except:
            authors_status.append(np.NaN)
        
        try:
            authors_ratings.append(result.find('div', class_='business-review-view__rating').\
                                       find('span', attrs={'itemprop': 'reviewRating'}).\
                                       find('meta', attrs={'itemprop': 'ratingValue'})['content'])
        except:
            authors_ratings.append(np.NaN)
        
        try:
            publication_date.append(result.find('span', class_='business-review-view__date').\
                                    find('meta')['content'])
        except:
            publication_date.append(0)
    
    authors_ratings_int = [float(n) for n in authors_ratings]

    data = pd.DataFrame.from_dict({'author': authors,\
                               'status': authors_status,\
                               'rating': authors_ratings_int,\
                               'publication_date': publication_date,\
                               'review': reviews})
    data['publication_date'] = pd.to_datetime(data['publication_date']).dt.date

    return data