import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
import time

data_list = []

def fetch_data(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    response = requests.get(url, headers = header)#headers是關鍵字
    soup = BeautifulSoup(response.text, "html.parser")
    names = soup.find_all("div", class_="main_con js-product-block")
    for name in names:
        data = {}
        data["品牌"] = "net"
        data["性別"] = s
        cloth_name = name.find("div", class_="main_name")
        cloth_name = cloth_name.a.text
        data["服飾名稱"] = cloth_name
        if name.find("span", class_="price_orginal"):
            price = name.find("span", class_="price_orginal")
            price = price.text
            data["價格"] = price
        else:
            price = name.find("span", class_="price_special")
            price = price.text
            data["價格"] = price
        img_src = name.find("div", class_="main_img").find("img", class_="js-product-img")
        img_src = img_src.get("src") 
        data["圖片網址"] = img_src
        buy_href = name.find("div", class_="main_img").a.get("href")
        data["購買網址"] = buy_href
        data_list.append(data)
    next_page = soup.find("div", class_="yahoo").find("a", class_="number_line_a page_next")
    if next_page:
        next_url = next_page.get("href")
        print("正在爬取:{}".format(next_url))
        fetch_data(next_url)

url = "https://www.net-fashion.net/category/2106"
s = "男"
fetch_data(url)
url = "https://www.net-fashion.net/category/2105"
s = "女"
fetch_data(url)

with open("NET.json", "w", encoding = "utf-8") as file:
    json.dump(data_list, file, ensure_ascii=False, indent=4)
