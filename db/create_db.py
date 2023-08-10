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

import pandas as pd

data = pd.read_csv('../db/links.csv', delimiter=',', index_col=0)
print('hello' in data['url'].values)
