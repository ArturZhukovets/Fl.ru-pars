import datetime
from collections import namedtuple

import urllib.parse
import bs4
import requests


from django.core.management.base import BaseCommand
from admin_panel.models import Apartment


InnerBlock = namedtuple('Block', 'title, price, date, url')


class Block(InnerBlock):

    def __str__(self):
        return f'{self.title}\t{self.price}\t{self.date}\t{self.url}'


class AvitoParser:
    """Session - сессия запросов, которая хранит в себе промежуточное состояние (куки, локалсы, заголовки и т.д)"""
    def __init__(self, clear=True) -> None:
        if clear:
            self.clear_storage()
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            'Accept-lenguage': "ru",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }

    def get_page(self, page:int = None):
        """Downloads the html web-page
        У session.get Есть атрибут парамс, в который передается словарь с параметрами урл запроса """

        params = {
            # serch filters
        }

        if page and page > 1:
             params['page'] = page # If page param is exist and page > 1

        url = "https://realt.by/rent/flat-for-long/"  # url without any params

        r = self.session.get(url, params=params)

        return r.text    

    
    def get_blocks(self, page:int = None):
        text = self.get_page(page=page) # Get the whole html
        soup = bs4.BeautifulSoup(text, 'lxml')
        
        # Запрос Css-селектора состоящего из множества классов, производится через select. Если один класс то используем find_all ->
        container = soup.find_all(class_="listing-item")
        for item in container:
            if len(item.find_all('div')) != 1:     # Исключаем рекламные блоки 
                block = self.parse_block(item=item)
                print(block, "\n-------------------")



    def parse_block(self, item):
        """item - soup object"""
        # Выбрать блок со ссылкой


        url_block = item.find(class_='teaser-tile teaser-tile-right').find('div', class_='desc').find('a')
        if url_block:
            url = url_block.get('href')
            title = url_block.string.strip()
        else:
            url = None

        # Выбрать блок с ценой. Альтернатива: price_block = item.find('div', class_="col-auto text-truncate")
        price_block = item.select_one('div.text-truncate')
        if price_block:
            price = price_block.text.strip()
            price_to_db = price.replace("BYN/месяц", '', 1).replace(" ", '')
            price_to_db = int(price_to_db)
        else:
            price = None
        # Выбрать блок с датой 
        date_block = item.select_one('div.info-mini').find_all('span')[2]
        if date_block:
            str_date = date_block.text
            try:
                date_to_db = self.strtime_to_datetime(time=str_date)
            except (ValueError, Exception):
                print("Неверный формат даты")
                date_to_db = None
        else:
            str_date = None
        
        # create model to save all data to DB
        try:
            p = Apartment(
                title=title,
                price=price_to_db,
                date=date_to_db,
                url=url
            ).save()   
        except Exception as ex:
            print(ex)
        
        # Returned Block object
        return Block(
            title=title,
            price=price,
            date=str_date,
            url=url
        )


    def get_paggination_limit(self):
        """Returns the number of pages"""
        text = self.get_page() # first page for looking pagination panel
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.select('div.paging-list a')
        href = container[-1].get('href')
        if not href:
            return 1
        
        r = urllib.parse.urlparse(href)   # Парсим последнюю страницу, достать query
        params = urllib.parse.parse_qs(r.query)
        return int(params['page'][0])
        


    def parse_all(self):
        """Take information from all pages"""
        limit = self.get_paggination_limit() # returns number of the last page 

        print(f"Всего страниц: {limit}")
        for i in range(1, limit):
            self.get_blocks(page=i)

            print(f"[#info] - Страница номер {i} сохранена")

    def parse_number_of_pages(self, number_of_pages:int):
        """Take information from  the specified number of pages"""
        print(f"Всего страниц: {number_of_pages}")
        for i in range(1, number_of_pages):
            self.get_blocks(page=i)
            print(f"[#info] - Страница номер {i} сохранена")


    @staticmethod
    def strtime_to_datetime(time:str):
        to_datetime_obj = datetime.datetime.strptime(time, "%d.%m.%Y")   
        return to_datetime_obj     


    @classmethod
    def clear_storage(cls):
        """Очищает БД"""
        queryset = Apartment.objects.all()
        queryset.delete()


            

class Command(BaseCommand):
    """Для того чтобы данный скрипт стал командой его нужно ОБЯЗАТЕЛЬНО обернуть в класс Command И наследоваться от BaseCommand"""
    help = "Парсинг квартир в аренду"

    def handle(self, *args: any, **options: any):
        p = AvitoParser()
        p.parse_number_of_pages(number_of_pages=10) # Вызываем 10 страниц с сайта
        
        

