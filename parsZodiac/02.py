import requests
from bs4 import BeautifulSoup
import lxml
import sys
import json


def get_data():
    list_of_urls_with_horoscopes = []
    url = 'https://astroscope.ru/horoskop/mesachniy_goroskop/'
    cookies = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    req = requests.get(url=url, cookies=cookies)
    req.encoding = 'utf-8'

    soup = BeautifulSoup(req.text, 'lxml')
    urls = soup.find('div', class_='list-group list-group-flush').find_all('a', class_='list-group-item list-group-item-action text-primary')
    for url in urls[ 1:]:
        list_of_urls_with_horoscopes.append("https:" + url.get('href'))

    list_with_horoscope_text = []

    for zodiac_url in list_of_urls_with_horoscopes:
        req = requests.get(url=zodiac_url, cookies=cookies)
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text, 'lxml')
        all_text = soup.find('div', class_='contain').find_all('p')
        zodiac_name = zodiac_url.split('/')[5].split('-')[-1].split('.')[0]

        overall_text_with_horoscope = ''
        for main_content in all_text:
            overall_text_with_horoscope += main_content.text.strip()

        list_with_horoscope_text.append(
            {
                zodiac_name: overall_text_with_horoscope
            }
        )

    with open(r'C:\py\first\blog\data\horoscope_for_30_days.json', 'w', ) as file:
        json.dump(list_with_horoscope_text, file, indent=4, ensure_ascii=False)



def main():
    get_data()


if __name__ == '__main__':
    main()
