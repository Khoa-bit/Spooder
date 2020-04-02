from web_scrape import scrape_wiki, grab_wiki_game_table, my_range


print("==============Hi! I'm Spooder==============")
year = input("Choose a year from 2014 to 2019 (e.g. 2019): ")
url = 'https://en.wikipedia.org/wiki/The_Game_Awards_' + year
print(">>> Your request will be saved in: " + "The_Game_Awards_" + year + ".csv (Same folder with main.py) <<<")
print("...........................................")

print(f"==============The game award {year}==============")
print("1. Game of the year")
print("2. All awards (Avg: 3 minutes)")
mode = input("Enter a number to choose: ")

print("==============Running... :3==============")
scrape_wiki(year, mode)
