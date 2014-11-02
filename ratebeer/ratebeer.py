from bs4 import BeautifulSoup
import requests
from pprint import pprint

class RateBeer():
    def __init__(self):
        self.BASE_URL = "http://www.ratebeer.com"

    def search(self, query):
        # this feels bad to me
        # but if it fits, i sits
        payload = {"BeerName": query}
        r = requests.post(self.BASE_URL+"/findbeer.asp", data = payload)
        return BeautifulSoup(r.text)

    def parse(self, soup):
        s_results = soup.find_all('table',{'class':'results'})
        output = {"breweries":[],"beers":[]}
        # find the brewery information
        if any("brewers" in s for s in soup.find_all("h1")):
            s_breweries = s_results[0].find_all('tr')
            for row in s_breweries:
                location = row.find('td',{'align':'right'})
                output['breweries'].append({
                    "name":row.a.contents,
                    "url":row.a.get('href'),
                    "location":location.contents[0].strip()
                })
        # find beer information
        if any("beers" in s for s in soup.find_all("h1")):
            s_beers = iter(s_results[1].find_all('tr'))
            next(s_beers)
            for row in s_beers: 
                link = row.find('td','results').a
                align_right = row.find_all("td",{'align':'right'})
                output['beers'].append({
                    "name":link.contents,
                    "url":link.get('href'),
                    "rating":align_right[-2],
                    "num_ratings":align_right[-1]
                    })
        return output

    def beer(self, name):
        pass

    def brewery(self, name):
        pass