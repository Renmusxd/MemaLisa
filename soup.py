from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

URL = "https://www.google.com/search?hl=en&site=imghp&tbm=isch&source=hp&q="
URL_PAGE = "&start="
query = "impressionism"
curr_page = 0


imgs = set()

while curr_page < 100:

	req = Request(URL + query + URL_PAGE + str(curr_page) ,headers={ 'User-Agent' : 'Mozilla/5.0' })
	html = urlopen(req)

	soup = BeautifulSoup(html)


	for i in soup.find_all("img", limit=100):
		imgs.add(i.get('src'))
		print(i.get('src'))

	curr_page = len(imgs)

print(len(imgs))