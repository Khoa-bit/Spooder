from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from process_game_links import process_a_link
from time import sleep


def web_scrape_for_game_awards(url, year):
    # Get and request Wiki's url
    print("Connecting to: " + url)
    wiki_url = urlopen(url).read()
    # Parse requested url
    soup = bs(wiki_url, "html.parser")
    # Wait
    print("Established!")
    sleep(1)
    # Look for games table
    tables = soup.findAll("table")
    games_table = tables[2].findAll("tr")

    # Store table in csv
    filename = "The_Game_Awards_" + year + ".csv"
    with open(filename, 'w') as f:
        print("Created " + filename)
        # 1st row of table
        # Grab Game of the year table title
        title = games_table[0].th.span.a.text
        f.write(title.upper() + ",")
        f.write("Link,")
        f.write("Developer(s),")
        f.write("Publisher(s),")
        f.write("Platform(s),")
        f.write("Release,")
        f.write("Genre(s),")
        f.write("Mode(s),")
        f.write("\n")

        # Grab table contents and process each content.

        game_of_the_year = games_table[1].td.ul.li.i.text
        # Grab link and process it
        game_of_the_year_link = 'https://en.wikipedia.org' + games_table[1].td.ul.li.i.b.a.get('href')
        processed_data = process_a_link(game_of_the_year_link)
        # Write to csv file
        f.write(game_of_the_year.upper() + "," + game_of_the_year_link + "," + processed_data + "\n")
        sleep(1)

        honourable_mentions = games_table[1].td.ul.li.ul.findAll("li")
        for honourable_mention in honourable_mentions:
            game = honourable_mention.i.text
            # Grab link and process it
            game_link = 'https://en.wikipedia.org' + honourable_mention.i.a.get('href')
            processed_data = process_a_link(game_link)
            # Write to csv file
            f.write(game + "," + game_link + "," + processed_data + "\n")
            sleep(1)
