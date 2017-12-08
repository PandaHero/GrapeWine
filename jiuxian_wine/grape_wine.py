from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# 获取浏览器驱动
driver = webdriver.Chrome()
# Load页面需要一段时间，设置一个默认等待时间
driver_wait = WebDriverWait(driver, 10)


# 进入主界面，key:商品名称
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
        # get_goods_contents()
    except TimeoutError:
        next_page(page_num)


# 获取网页源代码
def get_goods_contents():
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    html = soup.find("div", {"class": "bjlineSmall"})
    print(html)


# 程序入口
def main():
    key = "奥莫斯-西拉红葡萄酒 750ml/瓶"
    total_goods_num = search(key)
    tem = 0
    if total_goods_num > 28:
        for page_num in range(1, int(total_goods_num / 28) + 1):
            if tem <= 3:
                next_page(page_num)
                get_goods_contents()
            tem+=1


if __name__ == '__main__':
    main()
