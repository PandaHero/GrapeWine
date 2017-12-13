import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

goods_info = []
proxy = requests.get("http://127.0.0.1:5010/get/").text
proxies = {"http": "http://" + str(proxy)}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server=" + str(proxies["http"]))

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(
    "http://s.manmanbuy.com/Default.aspx?PageID=1&smallclass=0&ppid=0&siteid=&searchmode=0&f1=0&f2=0&f3=0&f4=0&f5=0&f6=0&price1=0&price2=0&orderby=score&iszy=0&istmall=0&zdj=0&key=%b0%c2%c4%aa%cb%b9-%ce%f7%c0%ad%ba%ec%c6%cf%cc%d1%be%c6+750ml%2f%c6%bf&v=&k=&min=&max=&w=&w2=&ft=&ft2=&distype=0")
soup = BeautifulSoup(driver.page_source, "lxml")
goods_lists = soup.find_all("div", {"class": "bjlineSmall"})
for goods in goods_lists:
    print(goods)
    print("--------------------------------------------")
    title_html = goods.find("div", {"class": "title"})
    price_html = goods.find("div", {"class": "cost"})
    comment_html = goods.find("div", {"class": "comment"})
    mall_html = goods.find("div", {"class": "mall"})
    goods_title = title_html.find("a", {"class": "shenqingGY"}).get_text().strip(" ")
    goods_price = price_html.find("span", {"class": "listpricespan"}).get_text().strip(" ")
    if comment_html:
        goods_comment = re.search("[1-9]\d*", str(comment_html.get_text()))
        if goods_comment:
            goods_comment = goods_comment.group(0)
    else:
        goods_comment = "无"

    goods_mall = mall_html.find("a", {"class": "shenqingGY"}).get_text().replace(" ", "")
    goods_url = title_html.find("a", {"class": "shenqingGY"})["href"]
    goods_mode = mall_html.find("p", {"class", "AreaZY"}).get_text()
    goods_info.append({"goods_title": goods_title})
    goods_info.append({"goods_url": goods_url})
    goods_info.append({"goods_price": goods_price})
    goods_info.append({"goods_comment": goods_comment})
    goods_info.append({"goods_mall": goods_mall})
    goods_info.append({"goods_mode": goods_mode})
print(goods_info)
