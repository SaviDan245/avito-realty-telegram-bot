# import sqlite3 as sql
#
#
# def main():
#     connection = sql.connect('realty.db')
#     cursor = connection.cursor()
#     cursor.execute("""
#         CREATE TABLE "offers" (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         title TEXT,
#         url TEXT,
#         offer_id INTEGER,
#         date TEXT,
#         price INTEGER,
#         adress TEXT,
#         area FLOAT,
#         rooms TEXT,
#         floor INTEGER,
#         total_floor INTEGER,
#         location_link TEXT
#         )
#     """)
#     connection.close()
#
#
# if __name__ == '__main__':
#     main()

REALTY_COLUMNS = [
    '№ п/п',
    'Название',
    'Ссылка на объявление',
    'ID объявления',
    'Дата публикации',
    'Цена',
    'Адрес',
    'Площадь помещения',
    'Количество комнат',
    'Этаж помещения',
    'Макс. этаж здания',
    'Ссылка на Google-карты'
]


import pandas as pd


data = [(1, '2-к. квартира, 54,5 м², 19/19 эт.', 'https://www.avito.ru/scherbinka/kvartiry/2-k._kvartira_545m_1919et._2354589727', 2354589727, '11.08.2023 в 13:48', 40000, 'Щербинка, ул. Барышевская Роща, 12', 54.5, '2-к. квартира', 19, 19, 'https://www.google.com/maps/search/?api=1&query=55.5032716653781,37.5390425638141'), (2, '1-к. квартира, 45 м², 7/9 эт.', 'https://www.avito.ru/himki/kvartiry/1-k._kvartira_45m_79et._1621972404', 1621972404, '11.08.2023 в 13:48', 32000, 'Химки, микрорайон Сходня, Первомайская ул., 19', 45.0, '1-к. квартира', 7, 9, 'https://www.google.com/maps/search/?api=1&query=55.95387415009396,37.30345224544212'), (3, '3-к. квартира, 59,6 м², 3/5 эт.', 'https://www.avito.ru/moskva/kvartiry/3-k._kvartira_596m_35et._3283242483', 3283242483, '11.08.2023 в 13:48', 60000, 'Москва, Валовая ул., 10', 59.6, '3-к. квартира', 3, 5, 'https://www.google.com/maps/search/?api=1&query=55.731293,37.631757'), (4, '1-к. квартира, 33,4 м², 4/6 эт.', 'https://www.avito.ru/mytischi/kvartiry/1-k._kvartira_334m_46et._3343721727', 3343721727, '11.08.2023 в 13:47', 27000, 'Мытищи, Тенистый б-р, 5', 33.4, '1-к. квартира', 4, 6, 'https://www.google.com/maps/search/?api=1&query=55.95881,37.673007'), (5, '1-к. квартира, 35 м², 9/12 эт.', 'https://www.avito.ru/scherbinka/kvartiry/1-k._kvartira_35m_912et._986953260', 986953260, '11.08.2023 в 13:46', 28000, 'Щербинка, ул. Барышевская Роща, 26', 35.0, '1-к. квартира', 9, 12, 'https://www.google.com/maps/search/?api=1&query=55.504986,37.534793')]

df = pd.DataFrame(data, columns=REALTY_COLUMNS)

df.to_excel('test.xlsx')
