from bs4 import BeautifulSoup
import json
import lxml
import re
import requests
from requests import Session
from threading import Thread





class WikipediaScraper():
    
    def __init__(self):
        self.base_url = "https://country-leaders.onrender.com"
        self.country_endpoint = "/countries"
        self.leaders_endpoint = "/leaders"
        self.cookie_endpoint = "/cookie"
        self.leaders_data = {}
        self.cookie = None
    

    def refresh_cookies(self):
        """"Function to ask for a new cookie"""
        self.cookie = requests.get(self.base_url + self.cookie_endpoint).cookies
    
    def get_countries(self):
        """Function to get the list of countries on the website"""
        countries = requests.get(self.base_url + self.country_endpoint, cookies = self.cookie).json()
        return countries
    

    def get_first_paragraph(self, session, wikipedia_url):
        """Tries to find the first paragraph from a wikipedia url which has bold letters and is larger then 50 characters"""
        # Make a request to get wikipedia content within a session.
        wikipedia = session.get(wikipedia_url).content

        # Put the content in a BeautifulSoup object to make use of its functions
        soup = BeautifulSoup(wikipedia, "lxml")

        # Find all p class elements and look if it has b class elements in it. 
        paragraphs = soup.find_all("p")
        for paragraph in paragraphs:
        # Break the loop if True to only get the first paragraph
            if paragraph.find_all("b") and len(paragraph.text) > 50:
                first_paragraph = paragraph.text
                break
        
        # Some regex to clean up first_paragraph.
        first_paragraph = re.sub("\[.*\]", "", first_paragraph)
        first_paragraph = re.sub(r"\n", "", first_paragraph)

        return first_paragraph


    
    def get_leaders(self):
        """Function first searches for the countries and then asks for the leaders of each country.
         We then loop through the country and ask the get_leaders_wiki to find the leaders, get the wikipedia url,
          use it to get its first paragraph and append it to the leader's dictionary."""
        
        # Ask for a new Cookie
        self.refresh_cookies()
        
        # Get countries from request.
        countries = requests.get(self.base_url + self.country_endpoint, cookies = self.cookie).json()
        
        # Create session for multiple requests
        with Session() as session:
            # Create threads for concurrency
            threads = list()
            for country in countries:
                thread = Thread(target = self.get_leaders_wiki, args=(session, country))
                threads.append(thread)
            # Starts the threads 
            for thread in threads:
                thread.start()
            # To close the threads
            for thread in threads:
                thread.join()


     
    def get_leaders_wiki(self, session, country):
        """This function first gets the leaders of the country, then loops for each leader, to get his wikipedia page,
        find the first paragraph and add it to the leader's dictionary before adding that to the self.Leaders_data attribute"""
        # Looks if cookies are still ok while trying to get country leaders for that country.
        try: 
            country_leaders = session.get(self.base_url + self.leaders_endpoint, params={"country": country}, cookies = self.cookie).json()

            if requests.get(self.base_url + self.country_endpoint, cookies = self.cookie).status_code == 403:
                raise CookieExpiredError("Cookie has expired") 
        except CookieExpiredError:
            print("Caught CookieExpiredError. Refreshing cookie...")
            self.refresh_cookies()
            country_leaders = session.get(self.base_url + self.leaders_endpoint, params={"country": country}, cookies = self.cookie).json()

        for country_leader in country_leaders:
            wikipedia_url = country_leader["wikipedia_url"]
            country_leader["first_paragraph"] = self.get_first_paragraph(session, wikipedia_url)
        self.leaders_data[country] = country_leaders

    
    def write_json(self):
        """ Writes the json object leaders_date previously declared in a json file"""
        # Makes it cleaner to read
        json_object = json.dumps(self.leaders_data, indent=4)

        with open("./data/leaders.json", "w") as file:
            file.write(json_object)


    def read_json(self):
        """Reads the previously written json file"""
        file_path = "./data/leaders.json"
        with open(file_path, "r") as file:
            data = json.load(file)
        print(data)

# Exception class for expired cookie error
class CookieExpiredError(Exception):
    pass    