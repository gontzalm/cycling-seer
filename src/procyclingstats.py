from bs4 import BeautifulSoup
from conf import BASE_URL
import requests


def is_active(soup):
    first_team = soup.select("ul[class='moblist rdr-teams'] li")[0].text.strip()
    return not ("Retired" in first_team)
    

def parse_rider(res):
    soup = BeautifulSoup(res.text, "html.parser")
    rdr_info = soup.select("div[class='rdr-info-cont']")[0]
    
    points = {}
    for sp in ["classic", "gc", "tt", "sprint", "climber"]:
        points[sp] = rdr_info.select(f"li.{sp} span:nth-child(2)")[0].text
    
    return {
        "nationality": rdr_info.find("a").text,
        "weight": rdr_info.find_all("span")[1].contents[1].strip().split(" ")[0],
        "height": rdr_info.select("span span")[0].contents[1].strip().split(" ")[0],
        "points": points,
        "img": soup.select("div[class='rdr-img-cont'] a img")[0]["src"],
        "active": is_active(soup)
    }


def get_rider(rider):
    url = f"{BASE_URL}/rider/{rider}"
    res = requests.get(url)

    if res.status_code != 200:
        return None
    else:
        rider_data = parse_rider(res)
        rider_data["name"] = rider.split("-")[0]
        rider_data["lname"] = rider.split("-")[1]
        return rider_data


def parse_race(res):
    pass


def get_race(race):
    pass