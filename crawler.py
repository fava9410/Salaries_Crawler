import requests
from lxml import html
from abc import ABC, abstractmethod

class Crawler(ABC):
    sep = '|'
    params = None
    url_site = None
    headers = None
    df = None

    def getConnection(self):
        try:
            response = requests.get(self.url_site, headers = self.headers, params = self.params)
            uu = response.raw
            vv = response.json()
            self.formatData(html.fromstring(response.text))
        except Exception as e:
            print(e)

    @abstractmethod
    def formatData(self):
        pass

    @abstractmethod
    def run(self):
        pass