import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
import re

data_list = []

def fetch_data(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    response = requests.get(url, headers = header)#headers是關鍵字
    soup = BeautifulSoup(response.text, "html.parser")
    names = soup.find_all("li", class_="row_before")
    for name in names:
        data = {}
        data["brand"] = "lativ"
        data["gender"] = s
        cloth_name = name.find("div", class_="productname")
        cloth_name = cloth_name.text
        data["clothname"] = cloth_name
        price = name.span
        price = price.text
        price = re.search(r"NT\$\d+", price).group()
        data["price"] = price
        img_src = name.find("a", class_="imgd").img.get("data-outfitpic")
        img_src = str(img_src).split(',')[0]
        data["img_src"] = "https://s1.lativ.com.tw"+str(img_src)
        buy_href = name.find("a", class_="imgd").get("href")
        data["buy_href"] = "https://www.lativ.com.tw/"+buy_href
        data_list.append(data)
   

url = [["https://www.lativ.com.tw/MEN", "男"],["https://www.lativ.com.tw/WOMEN", "女"]]
for i in url:
    s = i[1]
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    response = requests.get(i[0], headers = header)#headers是關鍵字
    soup = BeautifulSoup(response.text, "html.parser")
    categories = soup.find_all("ul", class_="sale_category")
    for category in categories:
        print(categories)
        li_hrefs = category.find_all("li")
        for li_href in li_hrefs:
            i[0] = li_href.a.get("href")
            print(i[0])
            fetch_data("https://www.lativ.com.tw"+i[0])


with open("lativ.json", "w", encoding = "utf-8") as file:
    json.dump(data_list, file, ensure_ascii=False, indent=4)