from bs4 import BeautifulSoup
import urllib
from urllib.request import Request, urlopen
import os

URL = "https://www.google.com/search?hl=en&site=imghp&tbm=isch&source=hp&q="
URL_PAGE = "&start="
queries = ["baroque+painting", "rococo+painting", "impressionism", "surrealism", "memes"]
curr_page = 100

for query in queries: 
	imgs = set()

	while curr_page < 300:

		req = Request(URL + query + URL_PAGE + str(curr_page) ,headers={ 'User-Agent' : 'Mozilla/5.0' })
		html = urlopen(req)

		soup = BeautifulSoup(html)

		for i in soup.find_all("img", limit=200):
			imgs.add(i.get('src'))

		curr_page = len(imgs)

	#os.mkdir("data/"+query)

	for i in range(len(imgs)):
		resource = urlopen(imgs.pop())
		output = open("data/"+query+"/"+query+"-img-"+str(i+100)+".jpg", "wb")
		output.write(resource.read())
		output.close()

	curr_page = 100;

