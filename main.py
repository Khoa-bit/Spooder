from web_scrape import scrape_wiki, grab_wiki_game_table, my_range
import timing


def list_award(games_table):
    count = 2
    for i in my_range(0, len(games_table) - 2, 2):
        for j in [1, 3]:
            award = games_table[i].contents[j].text.replace("\n", "")
            # Exclude not game table.
            formatted_title = award.replace("\n", "").upper()
            if (formatted_title == "BEST PERFORMANCE" or formatted_title == "DEVELOPER OF THE YEAR" or
                    formatted_title == "CONTENT CREATOR OF THE YEAR"):
                award += " (Not available)"
            print(f"{count}. " + award)
            count += 1


def main():
    print("==============Hi! I'm Spooder==============")
    year = input("Choose a year from 2014 to 2019 (e.g. 2019): ")
    url = 'https://en.wikipedia.org/wiki/The_Game_Awards_' + year
    print(">>> Your request will be saved in: " + "The_Game_Awards_" + year + ".csv (Same folder with main.py) <<<")
    print("...........................................")
    games_table = grab_wiki_game_table(year)

    print(f"\n==============The game award {year}==============")
    print("1. All awards (Avg: 3 minutes)")
    list_award(games_table)
    mode = input("Enter a number to choose: ")

    print("\n==============Running... :3==============")
    mode = int(mode)
    scrape_wiki(year, games_table, mode)


if __name__ == '__main__':
    main()
