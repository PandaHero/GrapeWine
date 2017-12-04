from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import requests

# 获取浏览器驱动
browser = webdriver.Chrome()
browser_wait = WebDriverWait(browser, 10)


# 浏览器加载主页面并返回包含关键字商品的总页数
def search():
    browser.get("https://www.jd.com")
    editText = browser_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#key")))
    button = browser_wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#search > div > div.form > button > i")))
    editText.send_keys("红酒")
    button.click()
    total_page_num = browser_wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > em:nth-child(1) > b"))).text
    return total_page_num


# 传入页码，并返回商品列表
def next_page(page_num):
    print("正在翻第" + str(page_num) + "页")
    # 获取页面右上角点击按钮
    button = browser_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_topPage > a.fp-next")))
    button.click()
    # 休息2秒获取下一个页面
    time.sleep(2)
    # 获取网页源代码
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    goodsList = soup.find("div", {"id": "J_goodsList"})
    # print(type(goodsList))
    lists = goodsList.find_all("li", {"class": "gl-item"})
    goods_info = []
    for goods in lists:
        goods_details = goods.find("div", {"class": "p-name p-name-type-2"})
        goods_price = goods.find("div", {"class": "p-price"})
        goods_url = goods.find("div", {"class": "p-img"})
        goods_commit = goods.find("div", {"class": "p-commit"})
        details = goods_details.a["title"]
        url = goods_url.a["href"]
        price = goods_price.get_text()
        commits = goods_commit.get_text()
        product = {"good_title": details, "good_url": url, "good_price": price, "good_commit": commits}
        goods_info.append(product)
        print(details, url, price, commits)
    return goods_info


# 解析每个商品url的信息，并返回商品详情页的数据：品牌、原产国、原料、产区等等
def get_details_info(url):
    product_details_info = []
    product_details_dic = {}
    req = requests.get(url)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, "lxml")
    # 获取商品的详细信息
    good_parameter = soup.find("div", {"class": "p-parameter"})
    parameter_brand = good_parameter.find("ul", {"id": "parameter-brand"}, {"class": "p-parameter-list"})
    brand = parameter_brand.find("li")["title"]
    p_parameter_list = good_parameter.find("ul", {"class": "parameter2 p-parameter-list"})
    li_parameter_list = p_parameter_list.find_all("li")
    # 把商品介绍的详情信息添加到product_details_info
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


if __name__ == '__main__':
    page_num = int(search())
    for num in range(1, page_num + 1):
        goods_info = next_page(num)
