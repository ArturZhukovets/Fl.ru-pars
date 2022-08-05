import requests
from bs4 import BeautifulSoup
import lxml
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}


def get_data_from_ziko():
    url = 'https://www.ziko.pl/wp-admin/admin-ajax.php?action=get_pharmacies'

    req = requests.get(url, headers=headers)
    response_in_json = json.loads(req.text)

    content = []
    for collection in response_in_json:
        obj = response_in_json[collection]
        data = {
            'name': obj['title'],
            'latlon': [(obj['lat'], obj['lng'])],
            'address': obj["address"],
            'working_hours': [(obj['mp_pharmacy_hours'].replace('<br>', ' ').rstrip()), obj['mp_pharmacy_enabled']]
        }
        content.append(data)

    with open('Test-task-RocketData/data/ziko.json', 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)


def get_data_from_monomah():
    url = 'https://monomax.by/map'
    req = requests.get(url, headers=headers)

    soup = BeautifulSoup(req.text, 'lxml')
    cards = soup.find_all('div', class_='shop')

    content = []
    for card in cards:
        data_dict = {
            'name': 'Мономах',
            'address': card.find('p', class_='name').text,
            'phones': [card.find('p', class_='phone').find('a').text],
        }
        content.append(data_dict)

    with open('Test-task-RocketData/data/monomah.json', 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)


def get_data_from_kfc():
    content = []
    url = 'https://api.kfc.com/api/store/v2/store.get_restaurants?showClosed=true'
    req = requests.get(url, headers=headers)
    json_data = json.loads(req.text)
    number_of_restaurant = len(json_data['searchResults'])
    print(number_of_restaurant)

    for restaurant_num in range(number_of_restaurant):
        try:
            road_to_inf = json_data['searchResults'][restaurant_num]['storePublic']['contacts']
            working_hours = json_data['searchResults'][restaurant_num]['storePublic']['openingHours']['regular']

            status = json_data['searchResults'][restaurant_num]['storePublic']['status']

            dict_data = {
                'address': [road_to_inf['streetAddress']['ru']],
                'latlon': road_to_inf['coordinates']['geometry']['coordinates'],
                "name": road_to_inf['coordinates']['properties']['name']['ru'],
                'phones': [road_to_inf['phone']['number']],
                "working_hours": [
                    f"пн-пт {working_hours['startTimeLocal']} до {working_hours['endTimeLocal']}"
                    f" сб-вс {working_hours['startTimeLocal']} до {working_hours['endTimeLocal']}",
                    status

                ],

            }
            content.append(dict_data)

            iterations_left = number_of_restaurant - restaurant_num
            print(f'Iteration number {restaurant_num} is gone. Iterations left {iterations_left} ')
        except TypeError:
            print(f'Object {restaurant_num} has some problems')
        except KeyError:
            print(f'Object {restaurant_num} has some with json keys')

    with open('Test-task-RocketData/data/kfc.json', 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)


def main():
    get_data_from_ziko()
    get_data_from_monomah()
    get_data_from_kfc()


if __name__ == '__main__':
    main()

