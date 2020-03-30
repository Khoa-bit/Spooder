from bs4 import BeautifulSoup as bs
from urllib.request import urlopen


# Get and request Wiki's url
url = 'https://en.wikipedia.org/wiki/The_Game_Awards_2019#Video_games'
wiki_url = urlopen(url).read()
# Parse requested url
soup = bs(wiki_url, "html.parser")
# Look for games table
tables = soup.findAll("table")
games_table = tables[2].findAll("tr")

# Store table in csv
filename = "games_of_the_year.csv"
with open(filename, 'w') as f:
    # Grab Game of the year table title
    title = games_table[0].th.span.a.text
    f.write(title.upper() + "\n")

    # Grab table contents
    game_of_the_year = games_table[1].td.ul.li.i.text
    game_of_the_year_link = 'https://en.wikipedia.org' + games_table[1].td.ul.li.i.b.a.get('href')
    f.write(game_of_the_year + "," + game_of_the_year_link + "\n")

    honourable_mentions = games_table[1].td.ul.li.ul.findAll("li")
    for honourable_mention in honourable_mentions:
        game = honourable_mention.i.text
        game_link = 'https://en.wikipedia.org' + honourable_mention.i.a.get('href')
        f.write(game + "," + game_link + "\n")
