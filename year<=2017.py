from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from process_game_links import process_a_link
from time import sleep


def find_n_clean_file(year):
    try:
        filename = "The_Game_Awards_" + year + ".csv"
        with open(filename, "r") as f:
            pass
    except IOError:
        pass
    else:
        # Clean existing csv file
        filename = "The_Game_Awards_" + year + ".csv"
        print("Cleaned " + filename)
        with open(filename, "w") as f:
            f.write("")


def process_store_data(table, side):
    # Choose num for table side.
    if side == "left":
        num = 1
    elif side == "right":
        num = 3

    # Store table in csv
    filename = "The_Game_Awards_" + year + ".csv"
    with open(filename, 'a') as f:
        print("Adding to " + filename)
        # 1st row of table
        # Grab Game of the year table title
        title = table[0].contents[num].text
        f.write(title.replace("\n", "").upper() + ",")
        f.write("Links,")
        f.write("Developer(s),")
        f.write("Producer(s),")
        f.write("Platform(s),")
        f.write("Release,")
        f.write("Genre(s),")
        f.write("Mode(s),")
        f.write("\n")

        # Grab table contents and process each content.

        game_of_the_year = table[1].td.ul.li.i.text
        # Grab link and process it
        game_of_the_year_link = 'https://en.wikipedia.org' + table[1].td.ul.li.i.b.a.get('href')
        processed_data = process_a_link(game_of_the_year_link)
        # Write to csv file
        f.write(game_of_the_year.upper() + " (1st)" + "," + game_of_the_year_link + "," + processed_data + "\n")
        # Wait a sec
        sleep(1)

        honourable_mentions = table[1].td.ul.li.ul.findAll("li")
        for honourable_mention in honourable_mentions:
            game = honourable_mention.i.text
            # Grab link and process it
            game_link = 'https://en.wikipedia.org' + honourable_mention.i.a.get('href')
            processed_data = process_a_link(game_link)
            # Write to csv file
            f.write(game + "," + game_link + "," + processed_data + "\n")
            # Wait a sec
            sleep(1)
        f.write("\n")


# Get and request Wiki's url
year = '2016'
url = 'https://en.wikipedia.org/wiki/The_Game_Awards_' + year
print("Connecting to: " + url)
wiki_url = urlopen(url).read()
# Parse requested url
soup = bs(wiki_url, "html.parser")
# Wait
print("Established!")
sleep(1)
# Look for games table
tables = soup.findAll("table")


if year == 2016:
    games_table = tables[2].findAll("tr")
else:
    games_table = tables[1].findAll("tr")

find_n_clean_file(year)

process_store_data(games_table, "left")
process_store_data(games_table, "right")
