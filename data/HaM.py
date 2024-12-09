from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json

data_list = []

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

urls = [
    "https://www2.hm.com/zh_asia3/men/shop-by-product/view-all.html?sort=stock&image-size=small&image=model&offset=0&page-size=3454",
    "https://www2.hm.com/zh_asia3/ladies/shop-by-product/view-all.html?sort=stock&image-size=small&image=model&offset=0&page-size=10000"
]

for url in urls:
    gender = "男" if "men" in url else "女"
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        names = soup.select("ul.products-listing li.product-item")
        for name in names:
            data = {}
            try:
                cloth_name = name.find("h3", class_="item-heading").text.strip()
                price = name.find("span", class_="price regular").text.strip()
                img_src = name.find("div", class_="image-container").find("img").get("data-altimage")
                buy_href = name.find("a", class_="item-link").get("href")
                data["brand"] = "H&M"
                data["gender"] = gender
                data["clothname"] = cloth_name
                data["price"] = price
                data["img_src"] = img_src
                data["buy_href"] = "https://www2.hm.com" + buy_href
                data_list.append(data)
            except AttributeError:
                continue
    except Exception as e:
        print(f"錯誤: {e}")

driver.quit()

with open("H&M.json", "w", encoding="utf-8") as file:
    json.dump(data_list, file, ensure_ascii=False, indent=4)
