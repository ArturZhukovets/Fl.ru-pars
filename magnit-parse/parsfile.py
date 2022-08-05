import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime
import lxml


URL = 'https://www.5ka.ru/special_offers/'


def collect_data(city_code='2398'):
    cur_time = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M')

    user_agent = UserAgent()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': user_agent.random,
    }
    cookies = {
        'mg_geo_id': f'{city_code}'
    }

    response = requests.get(url=URL, cookies=cookies)

    with open(f'index.html', 'w', encoding='utf-8') as file:
        file.write(response.text)

    with open(f'index.html', 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    #city = soup.find('button', class_='location-button focus-btn transparent').find('div', class_='focus-btn__content').text
    some_test = soup.find('div', class_='common-tabs__list').text
    print(some_test)




def main():
    collect_data(city_code='2398')


if __name__ == '__main__':
    main()