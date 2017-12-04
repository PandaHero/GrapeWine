import requests
import urllib.request
from bs4 import BeautifulSoup

product_details_info = []
product_details_dic = {}
req = requests.get("https://item.jd.com/10518564019.html")
soup = BeautifulSoup(req.text)
# 获取商品的详细信息
good_parameter = soup.find("div", {"class": "p-parameter"})
print(type(good_parameter))
parameter_brand = good_parameter.find("ul", {"id": "parameter-brand"}, {"class": "p-parameter-list"})
brand = parameter_brand.find("li")["title"]
p_parameter_list = good_parameter.find("ul", {"class": "parameter2 p-parameter-list"})
li_parameter_list = p_parameter_list.find_all("li")
for li_parameter in li_parameter_list:
    li_split = li_parameter.get_text().split(":")
    product_details_dic[li_split[0]] = li_split[1]
# 把商品的规格与包装信息添加到product_details_info
ptable = soup.find("div", {"class": "Ptable"})
ptable_dl = ptable.find("dl")
ptable_dt = ptable_dl.find_all("dt")
ptable_dd = ptable_dl.find_all("dd")
for i in range(len(ptable_dt)):
    product_details_dic[ptable_dt[i].get_text()] = ptable_dd[i].get_text()
for key ,value in product_details_dic.items():
    print(key,value)

content = urllib.request.quote("20000:34042")
print(content)
