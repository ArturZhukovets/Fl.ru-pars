import requests
from bs4 import BeautifulSoup
import lxml
import sys
import json


def get_data():
    list_of_words = []

    cookies = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }
    req = requests.get(url='https://englex.ru/english-for-engineers/', cookies=cookies)
    req.encoding = 'utf-8'

    soup = BeautifulSoup(req.text, 'lxml')
    all_tables = soup.find_all('table', class_='post-table')
    # print(all_tables, "\n\n\n\n")
    for content in all_tables:
        all_tr_in_one_table = content.find_all('tr')
        for words in all_tr_in_one_table:
            try:
                list_of_words.append(
                    {
                        'word': words.find('td').text,
                        'translate': words.find('td').next_sibling.text
                    }
                )
            except AttributeError:
                continue

    print(list_of_words)
    with open('eng_words.json', 'w', encoding='utf-8') as file:
        json.dump(list_of_words, file, indent=2, ensure_ascii=False)
print('sada')
get_data()

