import requests
from bs4 import BeautifulSoup

class WikiWorker:
    def __init__(self, url):
        self._url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    @staticmethod
    def _extract_symbols(page_html):
        soup = BeautifulSoup(page_html)
        table = soup.find(id="constituents")
        rows = table.find_all("tr")
        for row in rows[1:]: 
            symbol = row.find("td").text.strip("\n")
            yield symbol


    def get_sp_500_symbols(self):
        headers = {
            "User-Agent": "MyResearchBot/1.0 (anu@example.com)"
        }
        response = requests.get(self._url, headers=headers)
        print(response)
        if response.status_code != 200: 
            print("Couldn't get entries")
            return []
        
        yield from self._extract_symbols(response.text)

    
ww = WikiWorker("")
gen = ww.get_sp_500_symbols()
for _ in range(5):
    print(next(gen))