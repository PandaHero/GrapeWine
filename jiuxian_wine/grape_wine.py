import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

driver=webdriver.Chrome()
driver_wait=WebDriverWait(driver,10)
def search(key):
    driver.get("http://www.manmanbuy.com/")
    editText = driver_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#skey")))
    button = driver_wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "body > div.main-header > div > div.search > div > div.panel > form > div.sBtn > input")))
    editText.send_keys(key)
    button.click()
    total_goods_num = driver_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#resultcomment > span"))).text
    return int(total_goods_num)


def next_page(page_num):
    # 休息5秒钟跳转到另一页
    time.sleep(3)
    try:
        editText = driver_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#pagenum")))
        button = driver_wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#dispage > input[type="button"]:nth-child(7)')))
        # 清空输入框内容
        editText.clear()
        # 输入框输入内容
        editText.send_keys(page_num)
        # 点击按钮，发送
        button.click()
        # 判断当前页面是否是加载页面
        driver_wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#dispage > font"), str(page_num)))
        # html = driver.page_source
        # soup = BeautifulSoup(html, "lxml")
        # bjlineSmallGoods = soup.find_all("div", {"class": "bjlineSmall"})
    except TimeoutError:
        next_page(page_num)


# 解析网页源代码并获取商品信息：商品名称,商品url,商品价格，商品评论，商品来源、商品经营方式
def get_goods_lists():
    goods_info = []
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    goods_lists = soup.find_all("div", {"class": "bjlineSmall"})
    for goods in goods_lists:
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
        goods_info.append({"goods_price": goods_price})
        goods_info.append({"goods_comment": goods_comment})
        goods_info.append({"goods_mall": goods_mall})
        goods_info.append({"goods_mode": goods_mode})
    return goods_info


# 程序入口
def main():
    key = "奥莫斯-西拉红葡萄酒 750ml/瓶"
    total_goods_num = search(key)
    tem = 0
    if total_goods_num > 28:
        for page_num in range(1, int(total_goods_num / 28) + 1):
            if tem <= 3:
                next_page(page_num)
                goods_info = get_goods_lists()
                print(goods_info)
            tem += 1


if __name__ == '__main__':
    main()
