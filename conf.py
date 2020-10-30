import os
import dotenv


dotenv.load_dotenv()

DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME")
BASE_URL = "https://www.procyclingstats.com"
PROFILE_DIR = "../profiles"

# Scraping parameters
RACES = {
    "tour-de-france": [(2005, 2021), 21],
    "giro-d-italia": [(2000, 2021), 21],
    "vuelta-a-espana": [(2008, 2020), 21],
    "tirreno-adriatico": [(2019, 2021), 8],
    "paris-nice": [(2019, 2021), 8],
    "volta-a-catalunya": [(2019, 2020), 7],
    "dauphine": [(2019, 2021), 8],
    "tour-de-romandie": [(2019, 2020), 5],
    "tour-de-suisse": [(2019, 2020), 9]
}
