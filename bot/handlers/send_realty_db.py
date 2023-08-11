import sqlite3 as sql
from typing import List

import pandas as pd
from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from bot.utils import REALTY_FILEPATH, REALTY_COLUMNS, BUTTONS

router = Router()


@router.message(F.text == BUTTONS['send_realty_db'])
async def send_realty_db(message: Message):
    with sql.connect(REALTY_FILEPATH) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM offers
        """)
        data: List[tuple] = cursor.fetchall()

        df = pd.DataFrame(data, columns=REALTY_COLUMNS)
        df.to_excel('bot/files/realty_database.xlsx')

        file = FSInputFile('bot/files/realty_database.xlsx')
        await message.answer_document(file)
