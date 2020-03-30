from bs4 import BeautifulSoup
from urllib.request import urlopen


def process_a_link(link):
    print("Processing link: " + link)
    soup = BeautifulSoup(urlopen(link).read(), "html.parser")
    info_box = soup.find("table", {"class": "infobox hproduct"})
    list_o_contents = info_box.findAll("tr")

    # Developer(s)
    dev = list_o_contents[2].td.text

    # Producer(s)
    pro = list_o_contents[3].td.text

    # Platform(s)
    plat = str()
    platforms = list_o_contents[-4].findAll("li")
    if len(platforms) == 0:
        plat = list_o_contents[-4].td.text.replace(",", " ")
    else:
        for platform in platforms:
            plat += platform.text + " | "

    # Release Date
    date = str()
    check_date = list_o_contents[-3].findAll("li")
    if len(check_date) == 0:
        date = list_o_contents[-3].td.text.replace(",", " ")
    else:
        i = 1
        for each_date in check_date:
            date += each_date.text.replace(",", " ")
            if i % 2 == 0:
                date += " | "
            else:
                date += ": "
            i += 1

    # Genre
    genre = list_o_contents[-2].td.text.replace(",", " ")

    # Mode(s)
    mode = list_o_contents[-1].td.text.replace(",", " | ")

    print("Done!")
    processed_data = dev + "," + pro + "," + plat + "," + date + "," + genre + "," + mode
    return processed_data
