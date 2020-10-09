from bs4 import BeautifulSoup
from conf import BASE_URL
import requests


def is_active(soup):
    """Check if rider is active or retired."""
    first_team = soup.select("ul[class='moblist rdr-teams'] li")[0].text.strip()
    return not ("Retired" in first_team)
    

def parse_rider(res):
    """Parser rider from procyclingstats.com response."""
    soup = BeautifulSoup(res.text, "html.parser")
    rdr_info = soup.select("div[class='rdr-info-cont']")[0]
    
    # Nationality, weight and height
    nationality = rdr_info.find("a").text
    weight = rdr_info.find_all("span")[1].contents[1].strip().split("  ")[0]
    weight = weight.split(" ")[0]
    height = rdr_info.select("span span")[0].contents[1].strip().split("  ")[0]
    height = height.split(" ")[0]

    # Specialty points
    points = {}
    for sp in ["classic", "gc", "tt", "sprint", "climber"]:
        tag = rdr_info.select(f"li.{sp} span:nth-child(2)")[0]
        points[sp] = int(tag.text.strip())

    # Image
    img = soup.select("div[class='rdr-img-cont'] a img")[0]["src"]
    
    return {
        "nationality": nationality,
        "weight": int(weight),
        "height": int(float(height)*100),
        "points": points,
        "img": img, 
        "active": is_active(soup)
    }


def get_rider(rider):
    """Get rider from procyclingstats.com."""
    url = f"{BASE_URL}/rider/{rider}"
    res = requests.get(url)

    if res.status_code != 200:
        return res.status_code
    
    rider_data = {"name": rider}
    rider_data.update(parse_rider(res))
    return rider_data


def is_ttt(soup):
    """Check if stage is team time trial."""
    stage_info = soup.select("h2 span.blue")[0].text
    return "TTT" in stage_info


def is_itt(soup):
    """Check if stage is individual time trial."""
    stage_info = soup.select("h2 span.blue")[0].text
    return "ITT" in stage_info


def parse_result(res):
    """Parse stage result from procyclingstats.com response."""
    soup = BeautifulSoup(res.text, "html.parser")
    tags = soup.select("h2 span.red")
    winner_tag = soup.select("td > a[href]")
    
    # Check if stage exists
    if not tags or not winner_tag:
        return 404

    # Check if team time trial
    if is_ttt(soup):
        return None

    # Start-finish & distance
    start_finish = tags[0].text.split("\xa0")
    start_finish = " ".join([x.strip() for x in start_finish if x])
    distance = tags[1].text.strip("()k")

    # Winner
    winner = winner_tag[0]["href"].split("/")[-1]

    return {
        "start/finish": start_finish,
        "distance": float(distance),
        "time trial": is_itt(soup),
        "winner": winner
    }


def parse_profile(res):
    """Parse profile from procyclingstats.com response."""
    soup = BeautifulSoup(res.text, "html.parser")
    profile_tag = soup.select("div.statDivLeft img:first-of-type")

    # Check if profile exists
    if not profile_tag:
        return 404

    profile = profile_tag[0]["src"]
    return {
        "profile": profile
    }


def get_stage(race, year, number):
    """Get stage from procyclingstats.com."""
    # Get stage result
    url = f"{BASE_URL}/race/{race}/{year}/stage-{number}/result"
    res = requests.get(url)

    if res.status_code != 200:
        return res.status_code
    
    result = parse_result(res)
    if not result or isinstance(result, int):
        return result
        
    stage_data = {
        "race": race,
        "year": year,
        "number": number
    }
    stage_data.update(result)

    # Get stage profile
    url = f"{BASE_URL}/race/{race}/{year}/stage-{number}/today/profiles"
    res = requests.get(url)

    if res.status_code != 200:
        return res.status_code
    
    profile = parse_profile(res)
    if isinstance(profile, int):
        return profile
    
    stage_data.update(profile)

    return stage_data