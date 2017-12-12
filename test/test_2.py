from urllib.request import quote
# from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
quote_data = quote("电脑")
html = requests.get(
    "http://s.manmanbuy.com/Default.aspx?smallclass=0&ppid=0&siteid=3&searchmode=0&f1=0&f2=0&f3=0&f4=0&f5=0&f6=0&price1=0&price2=0&orderby=score&iszy=0&istmall=0&zdj=0&key=%b0%c2%c4%aa%cb%b9-%ce%f7%c0%ad%ba%ec%c6%cf%cc%d1%be%c6+750ml%2f%c6%bf&v=&k=&min=&max=&w=&w2=&ft=&ft2=&distype=0",
    headers=headers)
soup = BeautifulSoup(html.content, "lxml")
print(soup)
goods_lists = soup.find_all("div", {"class": "bjlineSmall"})


