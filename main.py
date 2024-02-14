#main.py
from src.scraper import WikipediaScraper

scraper = WikipediaScraper()

scraper.get_leaders()
scraper.write_json()
scraper.read_json()