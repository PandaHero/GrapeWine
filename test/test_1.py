import requests
import urllib.request
from bs4 import BeautifulSoup
con=requests.get("https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDA3MzkwMjUxOC5odG1s&log=5OQaV8S-C9sTu0BpsJg9zbSz_xpgmXTlWLUqmWcBb_Wb8G-ZNg0qCzdhrxqrAH5YklegJ50byriaqC6qSMpd1ROogwIJliQG8kKfrV8vSHrgHipNm4q1KJNWWZO5P4rMvfdzRhqgV1fnngMQV5gfyHrGHgDmYW5gHIXFXmGSCrRvqn5V3d4Ar-WOjZVBarbRFAmngOnYok8G1lx5wbBnjEfiZR0PRUZZA2cI6G2v6E5NJZCrarquG-PKYVJF65HWMTbIIYxvuOhfgvq5jD-zl2dAiEcrbYNWOutavrnwdZcXAzI7xqjTHeg7QERg2y7Typbrft5YdE_Gcr6kBlV0SEhLBjfbzN2WB97Y0iUL81dqzj5qEjX0orFsaL_LWbwGLZMdJfQONLxdiAVBnx96uPZd7G06QNp113FXIPa5c1aeq0JZ9ckWPryiBKvPEpqmDonCVOyFUrvDE7PpiIefVQ&v=404")
print(con.text)

product_details_info = []
product_details_dic = {}
req = requests.get("https://item.jd.com/10518564019.html")
soup = BeautifulSoup(req.text)
# 获取商品的详细信息
good_parameter = soup.find("div", {"class": "p-parameter"})
# print(type(good_parameter))
parameter_brand = good_parameter.find("ul", {"id": "parameter-brand"}, {"class": "p-parameter-list"})
brand = parameter_brand.find("li")["title"]
p_parameter_list = good_parameter.find("ul", {"class": "parameter2 p-parameter-list"})
li_parameter_list = p_parameter_list.find_all("li")
for li_parameter in li_parameter_list:
    li_split = str(li_parameter.get_text()).split("：")
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
# print(content)
