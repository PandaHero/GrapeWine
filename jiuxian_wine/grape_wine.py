from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re
import time
import requests
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
driver = webdriver.Chrome()
driver_wait = WebDriverWait(driver, 10)


def search(key):
    driver.get("http://www.manmanbuy.com/")
    edit_text = driver_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#skey")))
    button = driver_wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "body > div.main-header > div > div.search > div > div.panel > form > div.sBtn > input")))
    edit_text.send_keys(key)
    button.click()
    total_goods_num = driver_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#resultcomment > span"))).text
    return int(total_goods_num)


def next_page(page_num):
    # 休息3秒钟跳转到另一页
    print("我正在跳转到第" + str(page_num) + "页")
    time.sleep(5)
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
    #        # 判断当前页面是否是加载页面
    #        driver_wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#dispage > font"), str(page_num)))
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
        goods_skuid = goods["skuid"]
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
        goods_info.append({"goods_title": goods_title, "goods_url": goods_url, "goods_price": goods_price,
                           "goods_comment": goods_comment, "goods_mall": goods_mall, "goods_mode": goods_mode,
                           "goods_sku": goods_skuid})
    return goods_info


# 通过慢慢买网站获取的商品skuid拼接各电商商品的url链接
def parse_goods_url(goods):
    goods_mall = goods["goods_mall"]
    goods_url = goods["goods_url"]
    goods_skuid = goods["goods_sku"]
    if "天猫" in goods_mall:
        url = goods_url
        # print(url)
    elif "京东" in goods_mall:
        url = "http://item.jd.com/" + str(goods_skuid) + ".html"
        # print(url)
    elif "苏宁" in goods_mall:
        if "_" in goods_skuid:
            sku_id = str(goods_skuid).split("_")
            url = "https://product.suning.com/0000000000/" + str(sku_id[-1]) + ".html"
        else:
            url = "https://product.suning.com/0000000000/" + str(goods_skuid) + ".html"
        # print(url)
    elif "亚马逊" in goods_mall:
        url = "https://www.amazon.cn/gp/product/" + str(goods_skuid)
    elif "考拉" in goods_mall:
        url = "https://www.kaola.com/product/" + str(goods_skuid) + ".html"
    elif "国美" in goods_mall:
        url = "http://item.gome.com.cn/" + str(goods_skuid) + ".html"
    elif "飞牛" in goods_mall:
        url = "http://item.feiniu.com/" + str(goods_skuid) + "?e="
    else:
        url = goods_url
    return url


# 判断是否需要继续翻页
def judge_next_page(keywords, goods_title):
    tem = 0
    for title in goods_title:
        if keywords in title:
            tem += 1
        else:
            continue
    return float(tem / len(goods_title))


# 解析商品详情页信息
"""""""""""""""""""""""""""""""""""""""""""""""
goods_title:商品名称
goods_price:商品价格
goods_commit:商品评论数
goods_sales:商品销量
goods_mode:商品经营方式
goods_brand:商品品牌
goods_variety:商品种类
"""""""""""""""""""""""""""""""""""""""""""""""


# 解析每个电商的商品详情并进行匹配，调用每个电商的解析方式
# "goods_title": goods_title,
# "goods_url": goods_url,
# "goods_price": goods_price,
# "goods_comment": goods_comment,
# "goods_mall": goods_mall,
# "goods_mode": goods_mode,
# "goods_sku": goods_skuid
def parse_goods_detail(keywords, product_info):
    # print(product_info)
    for info in product_info:
        goods_mall = info["goods_mall"]
        # print(goods_mall)
        req = requests.get(info["goods_url"], headers=headers)
        if "天猫" in goods_mall:
            print("1", info["goods_url"])
            tmall_goods_detail_info = parse_tmall_goods_detail(req)
            info["品牌"] = tmall_goods_detail_info["品牌"]
            if "净含量" in tmall_goods_detail_info.keys():
                info["规格"] = tmall_goods_detail_info["净含量"]
            else:
                info["规格"] = "无"
            info["单位"] = tmall_goods_detail_info["套装规格"]
            yield info
        elif "京东" in goods_mall:
            print("2", info["goods_url"])
            jd_goods_detail_info = parse_jd_goods_detail(keywords, req)
            info["品牌"] = jd_goods_detail_info["品牌"]
            if "容量" in jd_goods_detail_info.keys():
                info["规格"] = jd_goods_detail_info["容量"]
            else:
                info["规格"] = "无"
            info["单位"] = "无"
            yield info
        elif "苏宁" in goods_mall:
            print("3", info["goods_url"])
            suning_goods_detail_info = parse_suning_goods_detail(keywords, req)
            info["品牌"] = suning_goods_detail_info["品牌"]
            if "净含量" in suning_goods_detail_info.keys():
                info["规格"] = suning_goods_detail_info["净含量"]
            else:
                info["规格"] = "无"
            info["单位"] = "无"
            yield info


"-----------------------------------------------------------------------"


# 解析天猫商品信息,并返回如下信息
# goods_brand:商品品牌
# goods_brand：净含量
# goods_size_suit:套装规格
# goods_variety:商品种类


def parse_tmall_goods_detail(req):
    dic_1 = {}
    soup = BeautifulSoup(req.content, "lxml")
    attributes = soup.find("div", {"id": "attributes"})
    goods_attrul = attributes.find("ul", {"id": "J_AttrUL"})
    goods_li = goods_attrul.find_all("li")
    for info in goods_li:
        text = str(info.get_text()).replace(" ", "").replace("：", ":").split(":")
        if text[0] == "净含量" or text[0] == "套装规格" or text[0] == "葡萄种类" or text[0] == "品牌":
            dic_1[text[0]] = text[-1]
    return dic_1


"-----------------------------------------------------------------------"


# 解析京东商品信息，并返回如下信息
# goods_brand:商品品牌
# goods_brand：净含量
# goods_size_suit:套装规格
# goods_variety:商品种类
def parse_jd_goods_detail(keywords, req):
    dic_1 = {}
    soup = BeautifulSoup(req.content, "lxml")
    good_parameter = soup.find("div", {"class": "p-parameter"})
    item_info = soup.find("div", {"class": "itemInfo-wrap"})
    # print(item_info)
    if item_info:
        sku_name = item_info.find("div", {"class": "sku-name"}).get_text().replace(" ", "").strip()

        parameter_brand = good_parameter.find("ul", {"id": "parameter-brand"})
        if parameter_brand:
            brand = parameter_brand.find("li")["title"]
            dic_1["品牌"] = brand
        else:
            dic_1["品牌"] = "无"
        #    dic_1["goods_name"]=sku_name
        if keywords in sku_name:
            if good_parameter:
                p_parameter_list = good_parameter.find("ul", {"class": "parameter2"})
                li_parameter_list = p_parameter_list.find_all("li")
                # 把商品介绍的详情信息添加到product_details_info
                for li_parameter in li_parameter_list:
                    li_split = str(li_parameter.get_text()).split("：")
                    if li_split[0] == "容量" or li_split[0] == "套装规格" or li_split[0] == "葡萄品种":
                        dic_1[li_split[0]] = li_split[-1]
        else:
            print("该商品不属于该品牌，错误")
    return dic_1


"-----------------------------------------------------------------------"


# 解析苏宁商品信息，并返回如下信息
# goods_brand:商品品牌
# goods_brand：净含量
# goods_size_suit:套装规格
# goods_variety:商品种类
def parse_suning_goods_detail(keywords, req):
    dic_1 = {}
    soup = BeautifulSoup(req.content, "lxml")
    proinfo_title = soup.find("div", {"class": "proinfo-title"})
    goods_name = proinfo_title.find("h1", {"id": "itemDisplayName"}).get_text().replace(" ", "").strip()
    procon_param = soup.find("div", {"class": "procon-param"})
    procon_tr = procon_param.find_all("tr")
    if keywords in goods_name:
        dic_1["品牌"] = keywords
        for tr in procon_tr:
            td_name = tr.find("td", {"class": "name"})
            if td_name:
                name = td_name.find("div", {"class": "name-inner"}).get_text()
                td_val = tr.find("td", {"class": "val"}).get_text()
                # print(name, td_val)
                if "净含量" in name or "葡萄品种" in name:
                    # print(td_val)
                    dic_1[name] = td_val
    else:
        print("该商品不属于该品牌，错误")
    return dic_1


"-----------------------------------------------------------------------"


# 解析亚马逊商品信息，并返回如下信息
# goods_brand:商品品牌
# goods_brand：净含量
# goods_size_suit:套装规格
# goods_variety:商品种类
# def parse_amazon_goods_detail(keywords, req):
#     pass


# 判斷該商品是否來源於天貓，淘寶，京東，舒寧，亞馬遜，考拉，國美，飛牛
def get_right_goods_info(goods_info):
    product_info = []
    for goods in goods_info:
        if "天猫" or "淘宝" or "京东" or "苏宁" or "亚马逊" or "考拉" or "国美" or "飞牛" not in goods["goods_mall"]:
            product_info.append(goods)
    return product_info


# 写入商品信息：商品名称,url,价格,评论數,品牌,规格,单位,商品来源,经营方式
def write_to_csv(info):
    with open(r"C:\Users\67505\Desktop\新建文件夹.csv", "a", newline="") as file:
        tem = 1
        writer = csv.writer(file)
        writer.writerow(
            ["goods_name", "url", "goods_price", "goods_commits", "brand", "size", "unit", "mall"])
        for goods in info:
            goods_name = goods["goods_title"]
            goods_url = goods["goods_url"]
            goods_price = goods["goods_price"]
            goods_commits = goods["goods_comment"]
            brand = goods["品牌"]
            size = goods["规格"]
            unit = goods["单位"]
            mall = goods["goods_mall"]
            if "京东" in brand:
                if "*" or "/" in goods_name:
                    pass
            goods_info = [goods_name, goods_url, goods_price, goods_commits, brand, size, unit,  mall]
            writer.writerow(goods_info)
            print("第" + str(tem) + "次写入成功")
            tem += 1
    print("写入完毕")


# 程序入口
def main():
    #    商品名称
    key = "奔富407干红葡萄酒750ml/瓶"
    #    商品品牌
    keywords = "奔富"
    total_goods_num = search(key)
    goods_title = []
    #    if total_goods_num > 28:
    for page_num in range(1, int(total_goods_num / 28) + 2):
        next_page(page_num)
        goods_info = get_goods_lists()
        for goods in goods_info:
            goods_url = parse_goods_url(goods)
            goods["goods_url"] = goods_url
            if page_num <= 3:
                goods_title.append(goods["goods_title"])
        scale = judge_next_page(keywords, goods_title)
        if scale > 0.25:
            print("scale=", scale)
            product_info = get_right_goods_info(goods_info)
            info = parse_goods_detail(keywords, product_info)
            write_to_csv(info)

        else:
            print("scale=", scale)
            break


if __name__ == '__main__':
    main()
