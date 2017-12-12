# coding = utf-8
import random
import time
import urllib.error
import urllib.request
import urllib.request

import gevent
from bs4 import BeautifulSoup
from gevent import monkey

home = "http://www.xicidaili.com/wt/"
first_proxy_list = []
end_proxy_list = []
# proxy_support = urllib.request.ProxyHandler({"http": "http://10.10.1.10:3128", "https": "http://10.10.1.10:1080"})
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"
}
monkey.patch_all()


def test_proxy(proxy_key):
    # for i in range(len(first_proxy_list)):
    # proxy_support = urllib.request.ProxyHandler({"http":proxy_list[i]})
    # print(proxy_key)
    proxy = {"http": proxy_key}
    url = "https://www.baidu.com/"

    proxy_support = urllib.request.ProxyHandler(proxy)
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    res = urllib.request.Request(url=url, headers=headers)
    try:
        response = urllib.request.urlopen(res, timeout=5)
        if response.code == 200:
            end_proxy_list.append(proxy_key)
    except Exception as e:
        print("error:", e)
    # except socket.timeout as e:
    #     print("This proxy is socket.timeout")
    # except urllib.error.URLError as e:
    #     print("This proxy is timeout")


def get_proxy_list():
    for i in range(20):
        url = home + str(i + 1)
        # print(url)
        # proxy_support = urllib.request.ProxyHandler({"http":"123.125.5.100:3128"})
        # opener = urllib.request.build_opener(proxy_support)
        # urllib.request.install_opener(opener)
        res = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(res, timeout=20).read().decode()
        soup = BeautifulSoup(response, 'html.parser')
        # print(response)
        content = soup.find_all("table", attrs={"id": "ip_list"})[0].find_all('tr')[1:]
        for i in range(len(content)):
            result = content[i].find_all('td')
            proxy_enum = result[1].text + ":" + result[2].text
            print(proxy_enum)
            first_proxy_list.append(proxy_enum)
        time.sleep(random.randint(120, 240))


def join_gevent(first_proxy_list, gevent_list):
    for i in range(len(first_proxy_list)):
        gevent_list.append(gevent.spawn(test_proxy, first_proxy_list[i]))


def main():
    gevent_list = []
    get_proxy_list()
    with open("proxy_first.txt", 'a', encoding='utf-8') as f:
        for item in first_proxy_list:
            f.write(item + '\n')
    join_gevent(first_proxy_list, gevent_list)
    gevent.joinall(gevent_list)
    # print(end_proxy_list)
    with open("proxy_end.txt", 'a', encoding='utf-8') as f:
        for item in end_proxy_list:
            f.write(item + '\n')


if __name__ == "__main__":
    main()
