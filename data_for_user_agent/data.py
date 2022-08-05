from bs4 import BeautifulSoup
import lxml
import requests


def get_data_ua():
    url = 'https://useragents.io/random?limit=200'
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    # response = requests.get(url, headers=headers)
    #
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)

    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'lxml')

    list_with_ua = soup.find_all('td')


    for ua in list_with_ua:
        result = ua.find('a').text + '\n'
        with open('data3.txt', 'a', encoding='utf-8') as f:
            f.writelines(result)




def main():
    get_data_ua()



if __name__ == '__main__':
    main()

