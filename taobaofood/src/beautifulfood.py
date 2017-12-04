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
#获取浏览器驱动
browser = webdriver.Chrome()
browser_wait = WebDriverWait(browser, 10)
#浏览器加载
def search():
    try:
#通过浏览器驱动加载url
        browser.get("https://www.taobao.com/")
#判断加载是否成功
#    获取输入框和点击按钮
        editText = browser_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        button = browser_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")))
        editText.send_keys("红酒")
        button.click()
        total_page = browser_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))).text
        print(total_page)
        return total_page
    except TimeoutException:
        return search()
def next_page(page_num):
    print("正在翻第" + str(page_num) + "页")
    try:
        editText = browser_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        button = browser_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
#        清除输入框中得内容
        editText.clear()
#        把页面数填入输入框
        editText.send_keys(page_num)
#        点击提交
        button.click()
#        判断当前页面是否是加载页面
        browser_wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page_num)))
        get_contents()
    except TimeoutError:
        next_page(page_num)
def get_goods_url():
    html = browser.page_source
    bs_obj = BeautifulSoup(html, "lxml")
    title_html = bs_obj.find_all("div", {"class":"row row-2 title"})
#    print(title_html, type(title_html))
    urls=[]
    for title_content in title_html:
        title_url = str(title_content.a["href"])
        if "http" in title_url:
            url = title_url
        else:
            url = "https:" + title_url
        urls.append({"url":url})
    return urls
def get_contents():
#    判断items(每一个宝贝)是否加载成功
    browser_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item")))
    html = browser.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()
#    print(items)
    products = []
    for item in items:
#        产品属性
        product = {"image":item.find('.pic .img').attr("data-src"), "price":item.find('.price').text(), "deal":item.find('.deal-cnt').text()[:-3], 'title':item.find('.title').text(), "shop":item.find(".shop").text()}
#        good_url = item.find('.title .a')
#        print(good_url)
        products.append(product)
#        browser.refresh()
    return products

def main():
    total_page = search()
    page_number = int(re.search("\d+", total_page).group())
#    print(page_number)
    products = []
    urls=[]
    for i in range(1, page_number + 1):
        next_page(i)
        products.append(get_contents())
        # 把每个商品详情页链接放入urls中
        urls.append(get_goods_url())

    with open("C:\\Users\\chen\\Desktop\\tbData.txt", "w+", encoding="utf-8") as file:
#        for goods in products:
#            print(goods,type(goods))
        print("正在写入文件：...")
        file.write("".join(str(products)))
    print("写入完成")
        
            
            
if __name__ == '__main__':
    main()
