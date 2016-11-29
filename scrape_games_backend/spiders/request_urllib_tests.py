import urllib.request
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime

def request_urllib_test(url):
	start = datetime.now()
	req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	page = urllib.request.urlopen(req).read()
	soup1 = BS(page, 'lxml-xml')
	end = datetime.now()
	print ("urllib-- xml --- %s --- %f" % (url,(end-start).total_seconds()))
	start = datetime.now()
	req = requests.get(url).content
	soup2 = BS(page, 'lxml-xml')
	end = datetime.now()
	print ("requests-- xml --- %s --- %f" % (url,(end-start).total_seconds()))
	print (soup1.prettify()==soup2.prettify())

if __name__ == '__main__':
	urls = ['https://www.gog.com/','https://www.bundlestars.com/', 'http://de.gamesplanet.com', 'https://www.direct2drive.com/', 'http://www.dlgamer.eu/', 'http://www.gamersgate.com', 'https://gamesrepublic.com/', 'https://www.greenmangaming.com', 'https://www.indiegala.com/store', 'https://store.steampowered.com', 'http://www.wingamestore.com/']
	for url in urls:
		request_urllib_test(url)
