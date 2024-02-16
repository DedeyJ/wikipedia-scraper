#main.py

# Import the WikipediaScraper module from scraper.py
from src.scraper import WikipediaScraper

# Initialize a WikipediaScraper object
scraper = WikipediaScraper()
# Looks up and writes away the leaders for each country. 
scraper.get_leaders()
# Writes away the data to a json file
scraper.write_json()
#Reads the file if found and prints in terminal
scraper.read_json()