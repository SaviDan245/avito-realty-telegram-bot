import sqlite3 as sql
from typing import Any

from termcolor import cprint


def update_database(offer: dict) -> bool:
    offer_id = offer['offer_id']

    with sql.connect('db/realty.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT offer_id FROM offers WHERE offer_id = (?)
        """, (offer_id,))
        result = cursor.fetchone()
        if result is None:
            # send_telegram(offer)
            cursor.execute("""
                INSERT INTO offers
                VALUES (NULL,
                :title, :url, :offer_id, :date, :price, :adress, :area, :rooms, :floor, :total_floor, :location_link)
            """, offer)
            connection.commit()
            # cprint(f'Объявление {offer_id} добавлено в базу данных', 'green')
            return True
        return False
