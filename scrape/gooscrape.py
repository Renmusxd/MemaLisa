import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


URL = "https://www.google.com/search?hl=en&site=imghp&tbm=isch&source=hp&q="

def queryGoogle(query):
    url = URL + query
    req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    r = urlopen(req).read()
    soup = BeautifulSoup(r,"html.parser")
    print(soup.prettify())
    print(soup.find('img',{'class':'rg_ic rg_i'}))
    return

queryGoogle('stuff')