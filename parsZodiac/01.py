import requests
from bs4 import BeautifulSoup
import lxml
import sys
import json


def get_data():
    url = 'https://astroscope.ru/'
    cookies = {
         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    req = requests.get(url=url, cookies=cookies)
    req.encoding = 'utf-8'
    #print(req.text)

    with open('index.html', 'w', encoding='utf-8-sig') as file:
        file.write(req.text)

    with open('index.html', 'r', encoding='utf-8') as file:
        src = file.read()

    list_of_cards_url = []
    soup = BeautifulSoup(src, 'lxml')
    zodiacs = soup.find('div', class_='container mb-3').find_all('a')
    for card in zodiacs:
        url = 'https://' + card.get('href').replace('//', '', 1)
        list_of_cards_url.append(url)
    content = []
    for zodiac in list_of_cards_url:
        req = requests.get(url=zodiac, cookies=cookies)
        req.encoding = 'utf-8'
        with open(f"{zodiac.split('/')[5]}", 'w', encoding='utf-8') as file:
            file.write(req.text)
        with open(f"{zodiac.split('/')[5]}", 'r', encoding='utf-8') as file:
            src = file.read()
        # req = requests.get(url=zodiac, cookies=cookies,)
        # # print(req.encoding)
        # req.encoding = 'utf-8'
        soup = BeautifulSoup(src, 'lxml')
        zodiac_name = f"{zodiac.split('/')[5].replace('.html', '')}"
        description_of_zodiac_sign = soup.find('div', class_='col-12').find('p').text.strip()
        content.append(
            {
                zodiac_name: description_of_zodiac_sign
            }
        )


    with open('horoscope.json', 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)
    #zodiac.split('/')[5].replace('.html', '')


def get_content_from_zodiac():
    pass


def main():
    get_data()


if __name__ == '__main__':
    main()
