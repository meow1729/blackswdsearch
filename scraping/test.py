from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://universe.bits-pilani.ac.in:12349/StudentSearch.aspx")
bsObj=BeautifulSoup(html.read(),"html.parser")
print(bsObj.html)
