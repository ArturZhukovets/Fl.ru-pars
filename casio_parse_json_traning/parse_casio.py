import time
import csv
import requests
from bs4 import BeautifulSoup
import lxml
import json
import os
from datetime import datetime


def get_all_pages():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

    }
    # url = 'https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/'
    # req = requests.get(url=url, headers=headers)
    #
    # if not os.path.exists('data'):   # Если указанный путь не существует, то создаем дирректорию
    #     os.mkdir('data')
    #
    # with open("data/page_1.html", 'w', encoding='utf-8') as file:
    #     file.write(req.text)

    with open("data/page_1.html", encoding='utf-8') as file:  # обязательно юзать encoding даже на чтение
        src = file.read()


    soup = BeautifulSoup(src, 'lxml')
    pages_count = soup.find('div', class_='bx-pagination-container').find_all("a")[-2]  # Собираю все ссылки и потом обращаюсь к предпоследней ссылке. Внутри неё был тег СПАМ с числом 4 - оно означает количество страниц на сайте
    pages_count = int(pages_count.text) # Преобразовал в ИНТ

    for i in range (1, pages_count +1):
        url = f'https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/?PAGEN_1={i}'

        req = requests.get(url=url, headers=headers)

        with open(f'data/page{i}.html', 'w', encoding='utf-8') as file:
            file.write(req.text)

            time.sleep(2)



    return pages_count + 1

def collect_data_from_all_pages(pages_count):
    """Важно для JSON!!! Создаю список data!!! Который потом пойдёт в Json формат. Заполню список словарями, затем
    открываю файл на запись Json и в него ложу мой список, кек."""
    cur_date = datetime.now().strftime('%d-%m-%Y')
    with open(f"data_{cur_date}.csv", 'w', encoding='utf-8') as file:   # Создаю заголовки для будущей таблицы CSV
        writer = csv.writer(file)
        writer.writerow(
            (
                "Артикул",
                "Ссылка",

            )
        )

    data = []                           # Создаю список под данные. В каждой итерации буду наполнять его словарями с новыми значениями
    for page in range(1, pages_count):
        with open(f"data/page{page}.html", 'r', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        items_cards = soup.find_all('a', class_='product-item__link')    # Список с карточками часов
        #print(items_cards)

        for item in items_cards: # забираем нужную инфу с карточек. На данный момент у меня список с контентом внутри тега <a>
            product_article = item.find('p', class_='product-item__articul').text.strip()
            product_url = item.get('href')
            # print(f"Article:{product_article}, URL: https://shop.casio.ru{product_url}")
            data.append(                    # заполняю список словарями
                {
                    "product_article": product_article,
                    "product_url": product_url,
                }
            )
            with open(f"data_{cur_date}.csv", 'a',
                      encoding='utf-8') as file:  # Здесь в цикле записываем данные в созданную таблицу. ПОМЕНЯТЬ ФЛАГ НА 'a'!!!
                writer = csv.writer(file)
                writer.writerow(
                    (
                        product_article,
                        product_url,

                    )
                )
            print(f"Обрабатываю страницу {page}/5")

        with open(f'data_{cur_date}.json', 'a', encoding='utf-8') as file:     # записываю вне цикла мой список в Json формат
            json.dump(data, file, indent=4, ensure_ascii=False)    # передаю в файл список, затем файл, отступ 4, и какую-то хуету.

        print("5/5 Страниц обработаны!")




def main():
    """"ЭТОТ СКРИПТ КАК МАНУАЛ К ПАРСИНГУ И РАБОТЕ С JSON И CSV ФОРМАТАМИ!"""
    pages_count = get_all_pages()
    collect_data_from_all_pages(pages_count=pages_count)


if __name__ == '__main__':
    main()