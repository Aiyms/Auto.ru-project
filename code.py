import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re
import datetime
import warnings
import numpy as np
import random

def get_request(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('span', class_ = 'ControlGroup ControlGroup_responsive_no ControlGroup_size_s ListingPagination-module__pages').find_all('a', class_= 'Button Button_color_whiteHoverBlue Button_size_s Button_type_link Button_width_default ListingPagination-module__page')[-1].get('href')
    total_pages = pages.split('=')[2]
    return int(total_pages)

def get_data(html): 
    r = requests.get(html)
    r.encoding = 'utf-8'
    id_auto = html[-10:]
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find('span', class_ = 'OfferPriceCaption__price')
    year = soup.find('a', class_ = 'Link Link_color_black')
    color = soup.find('a', class_ = 'Link Link_color_black')
    return id_auto, price, year, color

def main():
    url = 'https://auto.ru/cars/bmw/all/?output_type=list&page=1'
    base_url = 'https://auto.ru/cars/bmw/all/?output_type=list&'
    page_part = 'page='
    total_pages = get_total_pages(get_request(url))
    for i in range(1,3):#total_pages):
        url_gen = base_url + page_part + str(i) ### страницы с объявлениями  
        r = requests.get(url_gen)
        soup = BeautifulSoup(r.text, 'html.parser')
        ads = soup.find('div', 'ListingCars-module__container ListingCars-module__list').find_all('a', 'Link ListingItemTitle-module__link')
        v = len(ads)
        for j in range(1,v):
            ###  url объявлений
            html = soup.find('div', 'ListingCars-module__container ListingCars-module__list').find_all('a', 'Link ListingItemTitle-module__link')[j].get('href') 
            data = get_data(html)
            print(data)
            