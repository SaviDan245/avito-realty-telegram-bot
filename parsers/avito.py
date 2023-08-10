import json
from datetime import datetime
from typing import List, Union
from urllib.parse import unquote

import requests
from selectolax.parser import HTMLParser
from termcolor import cprint

from db.fetch_db import update_database

SITE = 'https://www.avito.ru'


def get_json(url: str) -> dict:
    """
    Получить JSON-словарь из HTML-кода страницы
    :param url: адрес поисковой строки с фильтрами и сортировкой по дате
    :return: JSON-словарь
    """
    response = requests.get(url)
    html = response.text

    tree = HTMLParser(html)
    scripts = tree.css('script')

    json_data: dict = {}

    for script in scripts:
        if 'window.__initialData__' in script.text():
            json_raw = unquote(script.text().split(';')[0].split('=')[1].strip().strip('"'))
            json_data = json.loads(json_raw)

    return json_data


def get_offer(item: dict) -> Union[None, dict]:
    """
    Распарсить оффер для добавления в базу данных
    :param item: JSON оффера
    :return: необходимые данные из оффера (в случае успеха)
    """
    try:
        timestamp = datetime.fromtimestamp(item['sortTimeStamp'] / 1000)

        city = item['geo']['geoReferences'][0]['content']
        adress = item['geo']['formattedAddress']
        coords = f'{item["coords"]["lat"]},{item["coords"]["lng"]}'

        raw_title = item['title'].split(', ')
        area = float(raw_title[1][:-2].strip().replace(',', '.'))
        rooms = raw_title[0]
        floor, total_floor = raw_title[2].split()[0].split('/')

        offer = {
            'title': item['title'].replace('\xa0', ' '),
            'url': SITE + item['urlPath'],
            'offer_id': item['id'],
            'date': datetime.strftime(timestamp, '%d.%m.%Y в %H:%M'),
            'price': item['priceDetailed']['value'],
            'adress': city + ', ' + adress,
            'area': area,
            'rooms': rooms,
            'floor': floor,
            'total_floor': total_floor,
            'location_link': 'https://www.google.com/maps/search/?api=1&query=' + coords
        }

    except:
        return None
    else:
        return offer


def upload_offers(data: dict) -> List[dict]:
    """
    Обновить базу данных новыми офферами
    :param data: JSON-словарь
    :return: список объявлений с необходимыми данными
    """
    target_key = None
    for key in data.keys():
        if 'single-page' in key:
            target_key = key
            break

    if target_key is None:
        raise (KeyError('Искомый ключ не найден в JSON'))

    for item in data[target_key]['data']['catalog']['items']:
        if item.get('id'):
            offer = get_offer(item)
            if offer:
                update_database(offer)
            else:
                cprint('Не удалось добавить оффер в базу данных.', 'red')


def main(url: str) -> None:
    json_data = get_json(url)
    upload_offers(json_data)


if __name__ == '__main__':
    main('https://www.avito.ru/moskva_i_mo/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&s=104')
