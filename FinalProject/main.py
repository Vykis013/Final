from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Nustatome webdriver'io kelią
webdriver_path = "C:/Users/Vykis/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(webdriver_path)
service.start()

# Sukuriamas naujas webdriver
driver = webdriver.Chrome(service=service)

# Funkcija, kuri paspaudžia "More" mygtuką ir laukia, kol bus įkelti nauji rezultatai
def click_more():
    try:
        more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ipc-see-more'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", more_button)
        more_button.click()

        # Laukiame, kol bus įkelti nauji rezultatai
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ipc-metadata-list-summary-item')))
    except Exception as e:
        pass

# Sukuriame sąrašą filmų
movies_list = []

url = "https://www.imdb.com/search/title/?title_type=feature"
driver.get(url)

# Puslapio scrolinimas
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)  # Ukrovimo laikas

# Paspaudžiame "See More" mygtuką 25 kartu
for i in range(25):
    click_more()
    # Scrollinam
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Laukiam kol uzkrauna

# Parsisiunčiame HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')
movies = soup.find_all('li', class_='ipc-metadata-list-summary-item')

for movie in movies:
    title = movie.find('h3', class_='ipc-title__text').text.strip()
    movie_details = movie.find_all('span', class_='sc-43986a27-8 jHYIIK dli-title-metadata-item')
    year = None
    duration = None
    rating = None

    if len(movie_details) >= 1:
        year = movie_details[0].text.strip()
    if len(movie_details) >= 2:
        duration = movie_details[1].text.strip()
    if len(movie_details) >= 3:
        rating = movie_details[2].text.strip()

    people_rating = movie.find('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating')
    people_rating_text = people_rating.get_text(strip=True).split('(')[0] if people_rating else None

    critic_rating = movie.find('span', class_='sc-b0901df4-0 bcQdDJ metacritic-score-box')
    critic_rating_text = critic_rating.get_text(strip=True) if critic_rating else None

    votes_element = movie.find('div', class_='sc-53c98e73-0 kRnqtn')
    votes_text = votes_element.text.strip() if votes_element else None

    # Jei 'Votes' nėra pateikti, priskiriame 'N/A'
    votes = 'N/A' if votes_text is None else f"{int(float(''.join(filter(str.isdigit, votes_text.replace(',', ''))))) :,}"

    movies_list.append({'Pavadinimas': title, 'Metai': year, 'Trukme': duration, 'Filmo indeksas': rating,
                        'Ivertinimas pagal zmones': people_rating_text, 'Ivertinimas pagal kritikus': critic_rating_text,
                        'Votes': votes})

# Uždarome webdriver
driver.quit()

# Sukuriame DataFrame ir išsaugome į CSV
df = pd.DataFrame(movies_list)
df.to_csv("IMDB25.csv", index=False)
print(df)