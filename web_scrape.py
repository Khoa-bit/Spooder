from bs4 import BeautifulSoup
from urllib.request import urlopen
from process_game_links import process_a_link
from time import sleep


def scrape_wiki(year, games_table, mode):
    find_n_clean_file(year)

    # Select mode
    award_num = 1
    if mode == 1:
        # All awards
        for i in my_range(1, len(games_table), 2):
            award_num = i
            process_store_data(year, games_table, award_num, "left")
            # Check whether right table exists.
            try:
                process_store_data(year, games_table, award_num, "right")
            except IndexError:
                pass
    else:
        # One award
        if mode % 2 == 0:
            side = "left"
            award_num = mode - 1
        if mode % 2 == 1:
            side = "right"
            award_num = mode - 2
        process_store_data(year, games_table, award_num, side)


def grab_wiki_game_table(year):
    # Get and request Wiki's url
    url = 'https://en.wikipedia.org/wiki/The_Game_Awards_' + year
    print("Connecting to: " + url)
    wiki_url = urlopen(url).read()
    # Parse requested url
    soup = BeautifulSoup(wiki_url, "html.parser")
    # Wait
    print("Established!")
    sleep(1)
    # Look for games table
    tables = soup.findAll("table")
    if year == "2017" or int(year) >= 2018:
        games_table = tables[2].findAll("tr")
    else:
        games_table = tables[1].findAll("tr")
    return games_table


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step


def find_n_clean_file(year):
    try:
        filename = "The_Game_Awards_" + year + ".csv"
        with open(filename, "r"):
            pass
    except IOError:
        pass
    else:
        # Clean existing csv file
        filename = "The_Game_Awards_" + year + ".csv"
        print("Cleaned " + filename)
        with open(filename, "w") as f:
            f.write("")


def process_store_data(year, table, award_id, side):
    # Choose num for table side.
    num = 1
    if side == "left":
        pass
    elif side == "right":
        num = 3

    # Store table in csv
    filename = "The_Game_Awards_" + year + ".csv"
    with open(filename, 'a') as f:
        # 1st row of table
        # Grab Game of the year table title
        title = table[award_id - 1].contents[num].text
        formatted_title = title.replace("\n", "").replace("[a]", "").replace("[b]", "").upper()

        # Exclude not game table.
        if (formatted_title == "BEST PERFORMANCE" or formatted_title == "DEVELOPER OF THE YEAR" or
                formatted_title == "CONTENT CREATOR OF THE YEAR"):
            return

        # Write the 1st row of table.
        print(f"Adding {formatted_title} award to {filename}")
        f.write(formatted_title + ",")
        f.write("Links,")
        f.write("Developer(s),")
        f.write("Publisher(s),")
        f.write("Platform(s),")
        f.write("Release,")
        f.write("Genre(s),")
        f.write("Mode(s),")
        f.write("\n")

        # Grab table contents and process each content.
        game_of_the_year = table[award_id].contents[num].ul.li.i.text

        # Try to grab link and process it.
        try:
            game_of_the_year_link = 'https://en.wikipedia.org' + table[award_id].contents[num].ul.li.i.b.a.get('href')
            processed_data = process_a_link(game_of_the_year_link)
            # Write to csv file.
            f.write(game_of_the_year.upper() + " (1st)" + "," + game_of_the_year_link + "," + processed_data + "\n")
        except AttributeError:
            # Write only name to csv file.
            f.write(game_of_the_year.upper() + " (1st),(No Link)" + "\n")
            print("No link to " + game_of_the_year)
            print("Skipped!")

        # Wait a sec
        sleep(1)

        honourable_mentions = table[award_id].contents[num].ul.li.ul.findAll("li")
        for honourable_mention in honourable_mentions:
            # Try to grab game title
            try:
                game = honourable_mention.i.text
            except AttributeError:
                # Not a game
                not_game = honourable_mention.a.text
                not_game_link = 'https://en.wikipedia.org' + honourable_mention.a.get('href')
                f.write(not_game + "," + not_game_link + ",(Not a game)" + "\n")
                print(not_game + " is not a game.")
                print("Skipped!")
                continue
            
            # Try to grab link.
            try:
                game_link = 'https://en.wikipedia.org' + honourable_mention.i.a.get('href')
            except AttributeError:
                # No link
                # Write only name to csv file.
                f.write(game + ",(No Link)" + "\n")
                print("No link to " + game)
                print("Skipped!")
                continue

            # Hard coded to skip
            # "Trover Saves the Universe", "Skylanders: Trap Team", "Ultra Street Fighter IV", "Fornite", "BattleTech"
            # due to complication of data.
            if (game == "Trover Saves the Universe" or game == "Skylanders: Trap Team" or
                    game == "Ultra Street Fighter IV" or game == "Fortnite" or game == "Nintendo Labo" or
                    game == "BattleTech"):
                f.write(game + "," + game_link + ",(Skipped due to complication)" + "\n")
                continue

            # Process link
            processed_data = process_a_link(game_link)
            # Write to csv file
            f.write(game + "," + game_link + "," + processed_data + "\n")
            # Wait a sec
            sleep(1)
        f.write("\n")
        f.write("\n")
