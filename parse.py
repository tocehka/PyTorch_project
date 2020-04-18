import requests
from bs4 import BeautifulSoup
from pathlib import Path
import urllib.request
import csv
import datetime

from utils import WriterManager
from config import *

conf = Config()
writer = WriterManager(file_name=conf.csv_file)
LABEL_CHECKER = "Артикул"
DELIMETR = "^"
RESOURSE_CONN_VERIFY_STR = "Ваша надежная торговая марка"
proxy = ProxyList()
proxies = proxy.get()

def get_page(url):
    try:
        r = requests.get(url)
        if RESOURSE_CONN_VERIFY_STR in r.text:
            return r.text
        else:
            raise Exception("e")
    except:
        print("Resourse banned default IP at " + datetime.datetime.now().isoformat())
        for proxy in proxies:
            proxy_item = {
                "http": "http://" + proxy,
                "https": "https://" + proxy
            }
            try:
                r = requests.get(url, proxies=proxy_item)
                return r.text
            except:
                print("Resourse banned " + proxy + " at " + datetime.datetime.now().isoformat())
                proxies.remove(proxy)
                continue

def get_items_url(category):
    page = get_page(conf.base_url + category)
    soup = BeautifulSoup(page, conf.xml_preprocessor)
    items_field = soup.find("ul", class_="catalog_list_main").find_all("div", class_="title")
    urls = []
    for item in items_field:
        for url in item:
            urls.append(url.get("href"))
            get_item_info(url.get("href"),category)

def get_item_info(url, category):
    page = get_page(conf.base_url + url)
    soup = BeautifulSoup(page, conf.xml_preprocessor)
    parsed_item_attributes_title = soup.find("div", class_="item_params").find_all("div", class_="title")
    parsed_item_attributes = soup.find("div", class_="item_params").find_all("div", class_="body")
    item_attributes = []
    label = ""
    if len(parsed_item_attributes_title) == len(parsed_item_attributes):
        for i in range(0, len(parsed_item_attributes)):
            title = parsed_item_attributes_title[i].getText().replace(":", "").strip()
            if title == LABEL_CHECKER:
                label = parsed_item_attributes[i].getText()
            item_attributes.append(title + DELIMETR + parsed_item_attributes[i].getText().strip())
    item_imgs = soup.find_all("a", class_="gal_zoom")
    item_attributes.append("images_path" + DELIMETR)
    for img in item_imgs:
        img_url = img.find("img").get("src").replace(conf.removing_part,'')
        if img == item_imgs[-1]:
            item_attributes[-1] = item_attributes[-1] + conf.img_dir + category + "/" + label + "/" + img_url.split("/")[-1]
            get_item_image(label, category, img_url)
            break
        item_attributes[-1] = item_attributes[-1] + conf.img_dir + category + "/" + label + "/" + img_url.split("/")[-1] + ","
        get_item_image(label, category, img_url)
    writer.write_row(item_attributes)

def get_item_image(label, category, img_url):
    label = "/" + label + "/"
    print(img_url)
    Path(conf.img_dir + category + "/" + label).mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(conf.base_url + img_url, conf.img_dir + category + label + img_url.split("/")[-1])

def main():
    page = get_page(conf.base_url)
    soup = BeautifulSoup(page, conf.xml_preprocessor)
    all_links = soup.find("ul", class_="children").find_all("li")
    for link in all_links:
        if len(link.find("a").get("href").split("/")) <= 3:
            category = link.find("a").get("href")
            print(category + "--------------------------------")
            Path("./images/" + category.replace("/","")).mkdir(parents=True, exist_ok=True)
            get_items_url(category)

main()