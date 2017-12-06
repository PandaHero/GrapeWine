import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://search.jd.com/s_new.php?keyword=%E7%BA%A2%E9%85%92&enc=utf-8&page=2&scrolling=y&show_items=1855313,302813,1772560,10865444154,636922,1304924,2150242,991778,11039059262,2214425,1182927,17212738322,1865339,636920,302817,2055132,11284806330,1175424,3564062,10810471452,1304915,3188580,636921,1175500,1865308,756154,3022178,1709853,3278417"
headers = {"Accept-Encoding": "gzip, deflate, sdch, br",
           "Accept-Language": "zh-CN,zh;q=0.8",
           "Connection": "keep-alive",
           "Cookie": "ipLoc-djd=1-72-2799-0; qrsc=3; user-key=fabc9ed1-34b6-4c47-905b-8a591c1584ff; cn=0; TrackID=1Cf0d8zDlNMi-Nh8fJzaxQHyuj6yY95ZNW997HP7tApYzeedW_TcPakelmURjH5SMG1fy9iSppcwzMedQOq1slM23N69mAYd2QiDZwZgH4Wg; pinId=zcvgUdwKIVIc3Mjva66NhLV9-x-f3wj7; pin=jd_638309812df29; unick=jd_188117vlqn; _tp=C6E1mKU%2FUrE9D%2Bsr77FDJPWRQmq6iENw%2Bqd0qhQpdpY%3D; _pst=jd_638309812df29; ceshi3.com=103; mt_xid=V2_52007VwMWUl5dUFMaSxBfBGIDEFZbUVpZGE0ZbAAzBhAGCFABRkhLTA4ZYgoWBUEIAAoZVREIUGNQEAJYCFRYHnkaXQVhHxJRQVlVSx9MEl8CbAMQYl9oUmofShpcBGEDEVdtWFdcGA%3D%3D; unpl=V2_ZzNtbRBTExUmWhFSKE0IVWIAFFVKB0oSc1tBV30dCwFkA0ZcclRCFXMURldnGFsUZwYZX0NcRxxFCEdkex5fDGQzFllDVkEcdgF2ZHgZbAVXAxZdQVJBHHAKT1d6HFwHYwUbVUFQRxVFOEFkexBYAWUDEG2WwujN%2fp8UFTnA7KCxqbxtRVJEE3wBQ1BLGGwEV1V8XUNWQhR9CURdfVRcAWcAF19LUkEcdglDVHkdWgxvABVZQmdCJXY%3d; __jdv=122270672|c.duomai.com|t_16282_55003828|tuiguang|c5a1bcf7beea42799a867b6275f521e0|1512541856677; thor=A257E4655512B33DC660E4CA52B913D703513485981E874E98F24A135E236C9D2E05DAD37089CFD0A8AD49B30AADA9000B6ECE5078C8BEF6AEDE0FB3498CC20A471BDA6A981307F835C719913EA1C62636B82C6B46A72FBAC7213AD77E72BE2F70B2705720AB37695921897FD2D0BDD06FC1CE08ECF381BE7F67B847D2A0D373E760E0E041DF62164EBF05510FA67F88F338945CA6200DE4E1E17042AE2400B9; __jda=122270672.15124384382041357892651.1512438438.1512539786.1512541857.10; __jdb=122270672.11.15124384382041357892651|10.1512541857; __jdc=122270672; xtest=3379.cf6b6759; rkv=V0200; __jdu=15124384382041357892651; 3AB9D23F7A4B3C9B=6PKO32CAWD4YZDHT5H5EBATJ4DT4RFKEQ7EFFJUQYW54U5N6ERCIHDRIVQV3WBCHYY5VFR6XJNEKH7WCVXHBD7RZAM",
           "Host": "search.jd.com",
           "Referer": "https://search.jd.com/Search?keyword=%E7%BA%A2%E9%85%92&enc=utf-8&suggest=1.his.0.0&wq=&pvid=76c46eeb71b0417e93d45d6900c4796f",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
           "X-Requested-With": "XMLHttpRequest"}
req = requests.get(url, headers=headers)
print(req.text)
# str=urllib.request.unquote("\u6021\u4e5d\u6021\u4e94\u9152\u7c7b\u4e13\u8425\u5e97")
# print(str)
html = urlopen(
    "https://search.jd.com/Search?keyword=%E7%BA%A2%E9%85%92&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&page=5&s=109&click=0")
# print(html.read())
soup = BeautifulSoup(html.read(), "lxml")
# print(soup)
goodsList = soup.find("div", {"id": "J_goodsList"})
# gl_warp = goodsList.find("ul",{"class":"gl-warp clearfix"})
items=goodsList.find_all("li")
show_items=""
for item in items:
    # if items.index(item) == -1:
    data_sku = item["data-sku"]
    show_items = show_items + str(data_sku) + ","
print(show_items[:-2])

