from Game_of_the_year_2019 import web_scrape_for_game_awards
from web_scrape_14to17 import web_scrape_14to17


year = input("Choose a year from 2014 to 2019: ")
url = 'https://en.wikipedia.org/wiki/The_Game_Awards_' + year
# web_scrape_for_game_awards(url, year)

if year <= "2017":
    web_scrape_14to17(year)
