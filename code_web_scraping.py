import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re
import datetime
import warnings
import numpy as np
import random
import csv

def get_request(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('span', class_ = 'ControlGroup ControlGroup_responsive_no ControlGroup_size_s ListingPagination-module__pages').find_all('a', class_= 'Button Button_color_whiteHoverBlue Button_size_s Button_type_link Button_width_default ListingPagination-module__page')[-1].get('href')
    total_pages = pages.split('=')[2]
    return int(total_pages)

def write_csv(data):
    with open('avito.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['productDate'],data['mileage'],data['bodyType'],data['color'],data['vehicleCondiguration'],data['vehicleTransmission'],data['Привод'],data['Руль'],data['Состояние'],data['Владельцы'],data['ПТС'],data['Таможня'],data['id'],data['price']))


def get_data(html): 
    r = requests.get(html)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    
    ### Добавляем ID
    id_auto = html[-10:] 
    
    ### Добавляем цену
    try:
        price = soup.find('span', class_ = 'OfferPriceCaption__price').getText().split()
        price = price[0]+ price[1] + price[2]
    except: 
        price = ''
    ### Cобираем данные с таблицы
    try:
        year = soup.find('ul', class_ = 'CardInfo').find_all('span')[1].text.strip()
    except:
        year = ''
    try:
        probeg = soup.find('ul', class_ = 'CardInfo').find_all('span')[3].text.strip() # Пробег
    except:
        probeg = ''
    try:
        kuzov = soup.find('ul', class_ = 'CardInfo').find_all('span')[5].text.strip() # Кузов
    except:
        kuzov = ''
    try:
        color = soup.find('ul', class_ = 'CardInfo').find_all('span')[7].text.strip()
    except:
        color = ''
    try:
        dvigate = soup.find('ul', class_ = 'CardInfo').find_all('span')[9].text.strip()# Двигатель
    except:
        dvigate = ''
    try:
        korobka = soup.find('ul', class_ = 'CardInfo').find_all('span')[13].text.strip() #Коробка
    except:
        korobka = ''
    try:
        privod = soup.find('ul', class_ = 'CardInfo').find_all('span')[15].text.strip() # Привод
    except:
        privod = ''
    try:
        rul = soup.find('ul', class_ = 'CardInfo').find_all('span')[17].text.strip() # Руль
    except:
        rul = ''
    try:
        sostoyanie = soup.find('ul', class_ = 'CardInfo').find_all('span')[19].text.strip() # Состояние
    except:
        sostoyanie = ''
    try:
        owners = soup.find('ul', class_ = 'CardInfo').find_all('span')[21].text.strip() # Владельцы
    except:
        owners = ''
    try:
        pts = soup.find('ul', class_ = 'CardInfo').find_all('span')[23].text.strip() # ПТС
    except:
        pts = ''
    try:
        tamozhnya = soup.find('ul', class_ = 'CardInfo').find_all('span')[25].text.strip() # Таможня
    except:
        tamozhnya = ''
    
    data = {'productDate': year,
            'mileage': probeg,
            'bodyType': kuzov,
            'color': color, 
            'vehicleCondiguration': dvigate,
            'vehicleTransmission': korobka,
            'Привод': privod,
            'Руль': rul,
            'Состояние': sostoyanie,
            'Владельцы': owners,
            'ПТС': pts,
            'Таможня': tamozhnya,
            'id': id_auto,
            'price': price
           }
    try: 
        d = write_csv(data)
    except: 
        d = ''
    return d


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
            
main()