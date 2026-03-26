from bs4 import BeautifulSoup
import requests
url = "https://bbs.archlinux.org/viewtopic.php?id=272247"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
print(soup.prettify())
