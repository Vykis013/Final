import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"}

movies_list = []

# Galime eiti per betkiek puslapiu
for page in range(1, 4):
    url = f"https://www.imdb.com/search/title/?title_type=feature&page={page}"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
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

df = pd.DataFrame(movies_list)
df.to_csv("imdbEGLv1.csv", index=False)
print(df)
