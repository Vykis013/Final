from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

URL = "https://www.imdb.com/list/ls503325184/"
driver.get(URL)

new_movies_list = []


def scrape_data():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    movies = soup.find_all('div', class_='lister-item-content')
    for movie in movies:
        title = movie.find('h3', class_='lister-item-header').text.strip()
        title_text = re.search(r"\n(.+)\n", title).group(1)
        years = movie.find('span', class_='lister-item-year text-muted unbold').text.strip().replace("(", "").replace(
            ")", "")
        length = movie.find('span', class_='runtime').text.strip().replace('min', '')
        genre = movie.find('span', class_='genre').text.strip()
        rating = movie.find('span', class_='ipl-rating-star__rating').text.strip()
        new_movies_list.append(
            {'Pavadinimas': title_text, 'Metai': years, 'Trukmė': length, 'Žanras': genre, 'Reitingas': rating})

def paspausti():
    try:
        load_more = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.lister-page-next.next-page'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", load_more)
        load_more.click()
        WebDriverWait(driver, 10).until(
            EC.staleness_of(load_more)
        )
    except Exception as e:
        print("Error while clicking 'Load More':", e)


scrape_data()

for _ in range(2):
    paspausti()
    scrape_data()

lentele = pd.DataFrame(new_movies_list)
print(lentele)
lentele.to_csv('imdbmod.csv', index=False)

driver.quit()