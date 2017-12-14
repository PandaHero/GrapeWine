import requests
from bs4 import BeautifulSoup

req = requests.get("https://product.suning.com/0070144563/169904807.html")
# soup = BeautifulSoup(req.content, "lxml")
# good_parameter = soup.find("div", {"class": "p-parameter"})
# item_info = soup.find("div", {"class": "itemInfo-wrap"})
# sku_name = item_info.find("div", {"class": "sku-name"}).get_text().replace(" ", "").strip()
# print(sku_name)
soup = BeautifulSoup(req.content, "lxml")
proinfo_title = soup.find("div", {"class": "proinfo-title"})
goods_name = proinfo_title.find("h1", {"id": "itemDisplayName"}).get_text().replace(" ", "").strip()
print(goods_name)
