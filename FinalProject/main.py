# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import pandas as pd
# import re
# import time
# import psycopg2
#
# # Aprasoma duombaze ir sukuriama lentele
# db_host = 'localhost'
# db_name = 'duomenubaze1'
# db_user = 'postgres'
# db_password = 'Vienetas1'
#
# connection = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
# cursor = connection.cursor()
# create_table_query = '''
#     CREATE TABLE IF NOT EXISTS imdb500(
#         id SERIAL PRIMARY KEY,
#         title text,
#         years text,
#         duration text,
#         rating text,
#         people_rating text,
#         critic_rating text,
#         votes text
#     )
# '''
# cursor.execute(create_table_query)
#
# # Nustatome webdriver'io kelią
# webdriver_path = "C:/Users/Vykis/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
# service = Service(webdriver_path)
# service.start()
#
# # Sukuriamas naujas webdriver
# driver = webdriver.Chrome(service=service)
#
#
# # Funkcija, kuri paspaudžia "More" mygtuką ir laukia, kol bus įkelti nauji rezultatai
# def click_more():
#     try:
#         more_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, 'ipc-see-more'))
#         )
#         driver.execute_script("arguments[0].scrollIntoView();", more_button)
#         more_button.click()
#
#         # Laukiame, kol bus įkelti nauji rezultatai
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '.ipc-metadata-list-summary-item')))
#     except Exception as e:
#         print(f"Error clicking 'More' button: {e}")
#         pass
#
#
# # Function to convert duration to minutes
# def convert_duration_to_minutes(duration):
#     if duration is None:
#         return None
#
#     # Extract hours and minutes using regular expression
#     match = re.match(r'(\d+)h\s*(\d*)m*', duration)
#
#     if match:
#         hours = int(match.group(1))
#         minutes = int(match.group(2)) if match.group(2) else 0
#         return hours * 60 + minutes
#     else:
#         return None
#
#
# # Sukuriame sąrašą filmų
# movies_list = []
#
# url = "https://www.imdb.com/search/title/?title_type=feature"
# driver.get(url)
#
# # Puslapio scrolinimas
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(5)  # Uzkrovimo laikas
#
# # Paspaudžiame "See More" mygtuką 5 kartus (pakeista iš 25 į 5)
# for i in range(5):
#     click_more()
#     # Scrollinam
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(6)  # Laukiam kol uzkrauna
#
# # Parsisiunčiame HTML
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# movies = soup.find_all('li', class_='ipc-metadata-list-summary-item')
#
# for movie in movies:
#     title_element = movie.find('h3', class_='ipc-title__text')
#     title = re.sub(r'^\d+\.\s*', '', title_element.text.strip()) if title_element else None
#
#     movie_details = movie.find_all('span', class_='sc-43986a27-8 jHYIIK dli-title-metadata-item')
#     year = None
#     duration = None
#     rating = None
#
#     if len(movie_details) >= 1:
#         year = movie_details[0].text.strip()
#     if len(movie_details) >= 2:
#         duration = movie_details[1].text.strip()
#         # Convert duration to minutes
#         duration = convert_duration_to_minutes(duration)
#     if len(movie_details) >= 3:
#         rating = movie_details[2].text.strip()
#
#     people_rating = movie.find('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating')
#     people_rating_text = people_rating.get_text(strip=True).split('(')[0] if people_rating else None
#
#     critic_rating = movie.find('span', class_='sc-b0901df4-0 bcQdDJ metacritic-score-box')
#     critic_rating_text = critic_rating.get_text(strip=True) if critic_rating else None
#
#     votes_element = movie.find('div', class_='sc-53c98e73-0 kRnqtn')
#     votes_text = votes_element.text.strip() if votes_element else None
#
#     # Jei 'Votes' nėra pateikti, priskiriame 'N/A'
#     votes = 'N/A' if votes_text is None else f"{int(float(''.join(filter(str.isdigit, votes_text.replace(',', ''))))) :,}"
#
#     # Jei 'Trukme' nėra pateikta, priskiriame 'N/A'
#     trukme = 'N/A' if duration is None else duration
#
#     movies_list.append({'Pavadinimas': title, 'Metai': year, 'Trukme': trukme, 'Filmo indeksas': rating,
#                         'Ivertinimas pagal zmones': people_rating_text,
#                         'Ivertinimas pagal kritikus': critic_rating_text,
#                         'Votes': votes})
#
#     # Irasome duomenis i SQL lentele
#     insert_query = '''
#         INSERT INTO imdb4(title, years, duration, rating, people_rating, critic_rating, votes) VALUES (%s, %s, %s, %s, %s, %s, %s)
#     '''
#     try:
#         cursor.execute(insert_query, (title, year, trukme, rating, people_rating_text, critic_rating_text, votes))
#         connection.commit()
#     except Exception as e:
#         print(f"Error inserting data into the database: {e}")
#
# # Uždarome webdriver
# driver.quit()
#
# # Sukuriame DataFrame ir išsaugome į CSV
# df = pd.DataFrame(movies_list)
# df.to_csv("imdb500.csv", index=False)
# print(df)
#
# # Uždarome duombazės prisijungimą
# cursor.close()
# connection.close()

# import pandas as pd
# import matplotlib.pyplot as plt
#
# df = pd.read_csv("imdb501.csv")
#
#
# df['Metai'] = pd.to_numeric(df['Metai'], errors='coerce')
#
# avg_ratings_by_year = df.groupby('Metai')[['Ivertinimas pagal zmones', 'Ivertinimas pagal kritikus']].mean()
#
# fig, ax1 = plt.subplots(figsize=(12, 6))
#
# ax1.plot(avg_ratings_by_year.index, avg_ratings_by_year['Ivertinimas pagal zmones'], label='People Rating', marker='o', color='green')
# ax1.set_xlabel('Year')
# ax1.set_ylabel('People Rating', color='green')
# ax1.tick_params(axis='y', labelcolor='green')
# ax1.set_ylim(1, 10)
#
# ax2 = ax1.twinx()
# ax2.plot(avg_ratings_by_year.index, avg_ratings_by_year['Ivertinimas pagal kritikus'], label='Critic Rating', marker='o', color='red')
# ax2.set_ylabel('Critic Rating', color='red')
# ax2.tick_params(axis='y', labelcolor='red')
# ax2.set_ylim(1, 100)
#
# plt.title('Average Ratings by Year')
# plt.show()
#
# import pandas as pd
# import matplotlib.pyplot as plt
#
# # Load data from CSV
# df = pd.read_csv("imdb501.csv")
# df['Metai'] = pd.to_numeric(df['Metai'], errors='coerce')
#
# # Group by 'Metai' and count the number of movies per year
# movies_per_year = df.groupby('Metai').size()
#
# # Plot bar chart
# fig, ax = plt.subplots(figsize=(12, 8))
#
# # Plot the total number of movies per year
# ax.bar(movies_per_year.index, movies_per_year, color='orange')
#
# # Show labels only every 5 years
# tick_positions = movies_per_year.index[::5]
# ax.set_xticks(tick_positions)
#
# # Rotate x-axis labels by 45 degrees
# ax.set_xticklabels(tick_positions, rotation=45, ha='right')
#
# # Add labels, title, and grid
# ax.set_xlabel('Year')
# ax.set_ylabel('Total Number of Movies')
# ax.set_title('Total Number of Movies Released per Year')
# ax.grid(axis='y', linestyle='--', alpha=0.7)
#
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
df = pd.read_csv("imdb501.csv")

# sortinam top10
top10_movies_critic = df.sort_values(by='Ivertinimas pagal kritikus', ascending=False).head(10)

# Votes to numeric
top10_movies_critic['Votes'] = top10_movies_critic['Votes'].apply(lambda x: pd.to_numeric(x.replace(',', ''), errors='coerce'))

# dydis
fig, ax1 = plt.subplots(figsize=(12, 8))

# pirma asis
color = 'tab:blue'
ax1.set_xlabel('Movies')
ax1.set_ylabel('Critic Rating', color=color)
ax1.bar(top10_movies_critic['Pavadinimas'], top10_movies_critic['Ivertinimas pagal kritikus'], label='Critic Rating', color=color)
ax1.tick_params(axis='y', labelcolor=color)

# antra asis
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('People Rating', color=color)
ax2.plot(top10_movies_critic['Pavadinimas'], top10_movies_critic['Ivertinimas pagal zmones'], label='People Rating', marker='o', color=color)
ax2.tick_params(axis='y', labelcolor=color)

# trecia asis
ax3 = ax1.twinx()
color = 'tab:green'
ax3.spines['right'].set_position(('outward', 60))
ax3.set_ylabel('Votes', color=color)
ax3.plot(top10_movies_critic['Pavadinimas'], top10_movies_critic['Votes'], label='Votes', marker='s', color=color)
ax3.tick_params(axis='y', labelcolor=color)

# pasukimas
ax1.set_xticklabels(top10_movies_critic['Pavadinimas'], rotation=45, ha='right')

# aprasymas
fig.suptitle('Top 10 Critically Acclaimed Movies with People Ratings and Votes')
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()

# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# # Load data from CSV
# df = pd.read_csv("imdb501.csv")
#
#
# df['Votes'] = pd.to_numeric(df['Votes'].str.replace(',', ''), errors='coerce')
#
#
# df_cleaned = df.dropna(subset=['Votes', 'Ivertinimas pagal zmones'])
#
#
# correlation = df_cleaned['Votes'].corr(df_cleaned['Ivertinimas pagal zmones'])
#
#
# plt.figure(figsize=(10, 6))
# sns.regplot(x='Votes', y='Ivertinimas pagal zmones', data=df_cleaned, scatter_kws={'s': 50}, line_kws={'color': 'red'})
# plt.title(f'Correlation between Votes and People\'s Ratings: {correlation:.2f}')
# plt.xlabel('Votes')
# plt.ylabel('People\'s Ratings')
#
# plt.show()

# import pandas as pd
# import numpy as np
# from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt
#
# # Nuskaitom CSV failą
# df = pd.read_csv("imdb501.csv")
#
# # Konvertuojam 'Metai' stulpelį į skaičius
# df['Metai'] = pd.to_numeric(df['Metai'], errors='coerce')
#
# # Filtruojam duomenis nuo 2000 metų ir netraukiam 'N/A' reikšmių ir NaN reikšmių
# df_filtered = df[df['Metai'] >= 2000]
# df_filtered = df_filtered[df_filtered['Votes'] != 'N/A']
# df_filtered = df_filtered.dropna(subset=['Votes'])
#
# # Konvertuojam Votes į skaičius
# df_filtered['Votes'] = df_filtered['Votes'].str.replace(',', '').astype(float)
#
# # Vidutiniškai balsuoja už kiekvienus metus
# avg_ratings_by_year = df_filtered.groupby('Metai')['Votes'].mean()
#
# # Sukuriam duomenų rinkinį
# X = avg_ratings_by_year.index.values.reshape(-1, 1)
# y = avg_ratings_by_year.values
#
# # Sukuriam tiesinę regresijos modelį
# model = LinearRegression()
# model.fit(X, y)
#
# # Prognozuokime balsus nuo 2024 iki 2035 metų
# future_years = np.array(range(2024, 2036)).reshape(-1, 1)
# predicted_votes = model.predict(future_years)
# predicted_votes = np.maximum(predicted_votes, 0)  # Nulis arba didesnis
#
# # Nupiešiam grafiką
# plt.plot(X, y, label='Vidutiniškai Balsuoja Už Metus', color='green', marker='o')
# plt.plot(future_years, predicted_votes, label='Prognozė (2024-2035)', color='orange', linestyle='dashed')
# plt.xlabel('Metai')
# plt.ylabel('Balsų Vidurkis')
# plt.legend()
# plt.show()