from bs4 import BeautifulSoup
from urllib.request import urlopen


def process_a_link(link):
    print("Processing link: " + link)
    soup = BeautifulSoup(urlopen(link).read(), "html.parser")
    info_box = soup.find("table", {"class": "infobox hproduct"})
    list_o_contents = info_box.findAll("tr")

    # Developer(s)
    dev = list_o_contents[2].td.text

    # Publisher(s)(s)
    pub = str()
    check_pub = list_o_contents[3].findAll("li")
    # No Show event.
    if len(check_pub) == 0:
        pub = list_o_contents[3].td.text.replace(",", " ")
    # List with [show] event
    elif list_o_contents[3].td.div.div:
        pub = list_o_contents[3].td.div.div.text.replace(",", " ").replace("[show]", "")
    # List without [show] event
    else:
        for each_date in check_pub:
            pub += each_date.text.replace(",", " ")
            pub += " | "

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
    # No Show event.
    if len(check_date) == 0:
        date = list_o_contents[-3].td.text.replace(",", " ")
    # List with [show] event excluding "plainlist" class.
    elif list_o_contents[-3].td.div.div:
        date = list_o_contents[-3].td.div.div.text.replace(",", " ").replace("[show]", "")
        # Delete style text.
        if list_o_contents[-3].td.div.div.style:
            date = date.replace(list_o_contents[-3].td.div.style.text, "")
        # Format 2017 plainlist
        if list_o_contents[-3].td.find("div", {"class": "plainlist"}):
            date = date.replace("2017PAL", "2017 | PAL")

    # List without [show] event
    else:
        i = 1
        for each_date in check_date:
            date += each_date.text.replace(",", " ")
            # No need to format if there is one <li> tag.
            if len(check_date) != 1:
                if i % 2 == 0:
                    date += " | "
                else:
                    date += ": "
                i += 1

    # Genre
    genre = list_o_contents[-2].td.text.replace(",", " ").replace("\n", "")

    # Mode(s)
    mode = list_o_contents[-1].td.text.replace(",", " | ")

    print("Done!")
    processed_data = dev + "," + pub + "," + plat + "," + date + "," + genre + "," + mode
    return processed_data
