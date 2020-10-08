import dotenv
import os


dotenv.load_dotenv()

DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")
BASE_URL = "https://www.procyclingstats.com"

# Scraping parameters
YEARS = (2007, 2020)