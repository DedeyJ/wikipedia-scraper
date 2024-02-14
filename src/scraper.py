from bs4 import BeautifulSoup
import json
import requests
from requests import Session




class WikipediaScraper():
    
    def __init__(self):
        self.base_url = "https://country-leaders.onrender.com"
        self.country_endpoint = "/countries"
        self.leaders_endpoint = "/leaders"
        self.cookie_endpoint = "/cookie"
        self.leaders_data = {}
        self.cookie = None
    

    def refresh_cookies(self):
        self.cookie = requests.get(self.base_url + self.cookie_endpoint).cookies
    
    def get_countries(self):
        countries = requests.get(self.base_url + self.country_endpoint, cookies = self.cookie).json()
        return countries
    

    def get_first_paragraph(self, session, wikipedia_url, date):
        wikipedia = session.get(wikipedia_url).content

        soup = BeautifulSoup(wikipedia, "html")

        paragraphs = [elem.text for elem in soup.find_all("p")]
        # for elem in soup.find_all("p"):
        #     paragraphs.append(elem.text)

        for paragraph in paragraphs:
            if date in paragraph:
                first_paragraph = paragraph
                break

        return first_paragraph



    def get_leaders(self):
        # Ask for a new Cookie
        self.refresh_cookies()
        countries = requests.get(self.base_url + self.country_endpoint, cookies = self.cookie).json()
        with Session() as session:
            for country in countries:
                try: 
                    country_leaders = session.get(self.base_url + self.leaders_endpoint, params={"country": country}, cookies = self.cookie).json()

                    if requests.get(self.base_url + self.country_endpoint, cookies = self.cookie).status_code == 403:
                        raise CookieExpiredError("Cookie has expired") 
                except CookieExpiredError:
                    print("Caught CookieExpiredError. Refreshing cookie...")
                    self.refresh_cookies()
                    country_leaders = session.get(self.base_url + self.leaders_endpoint, params={"country": country}, cookies = self.cookie).json()

                for i in range(len(country_leaders)):
                    wikipedia_url = country_leaders[i]["wikipedia_url"]
                    print(wikipedia_url)

                    if country_leaders[i]["birth_date"] is not None:
                        date = country_leaders[i]["birth_date"].split("-")[0]
                    elif country_leaders[i]["death_date"] is not None:
                        date = country_leaders[i]["death_date"].split("-")[0]
                    else:
                        date = country_leaders[i]["end_mandate"].split("-")[0]
                    country_leaders[i]["first_paragraph"] = self.get_first_paragraph(session, wikipedia_url, date)

                print(country_leaders)
                self.leaders_data[country] = country_leaders


    def write_json(self):

        json_object = json.dumps(self.leaders_data, indent=4)

        with open("./leaders.json", "w") as file:
            file.write(json_object)
    # Load the JSON data
            
    def read_json(self):
        with open("./leaders.json", "r") as file:
            data = json.load(file)
        print(data)

        
class CookieExpiredError(Exception):
    pass    