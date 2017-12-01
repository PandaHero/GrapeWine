'''
Created on 2017-11-7

@author: chen
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from selenium.common.exceptions import TimeoutException
import urllib.request

# 获取浏览器驱动
browser = webdriver.Chrome()
browser_wait = WebDriverWait(browser, 10)


# 浏览器加载
def search():
    try:
        # 通过浏览器驱动加载url
        browser.get("https://www.taobao.com/")
        # 判断加载是否成功
        #    获取输入框和点击按钮
        editText = browser_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        button = browser_wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")))
        editText.send_keys("红酒")
        button.click()
        total_page = browser_wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))).text
        # print(total_page)
        return total_page
    except TimeoutException:
        return search()


# 获取淘宝中红酒的所有品牌
def get_goods_brand():
    # 判断页面是否已经加载完毕
    browser_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item")))
    # 获取该网页源码
    html = browser.page_source
    # print(html)
    soup = BeautifulSoup(html, "lxml")
    brand_items = soup.find("div", {"class": "items items-show2line J_Items"})
    items_inner = brand_items.find("div", {"class": "items-inner g-clearfix"})
    items = items_inner.find_all("a", {"class": "item icon-tag J_Ajax "})
    # print(type(items))
    for item in items:
        brand_name = item.find("span", {"class": "text"}).get_text()
        url_name = item["data-value"]
        url_quote_name = urllib.request.quote(url_name)
        yield brand_name, url_quote_name


def get_goods_brand_url(brand_name, url_quote_name):
    url = "http://s.taobao.com/search?q=%E7%BA%A2%E9%85%92&ppath=" + str(url_quote_name)
    return url

def parse_goods_brand(url):
    browser.close()
def main():
    search()
    for brand_name, url_quote_name in get_goods_brand():
        url=get_goods_brand_url(brand_name, url_quote_name)
        print(url)
        browser.get(url)



if __name__ == '__main__':
    main()
