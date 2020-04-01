from Game_of_the_year_2019 import web_scrape_for_game_awards


year = input("Choose a year from 2014 to 2019: ")
url = 'https://en.wikipedia.org/wiki/The_Game_Awards_' + year
web_scrape_for_game_awards(url, year)
