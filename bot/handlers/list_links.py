import pandas as pd
from aiogram import Router, F
from aiogram.types import Message
from keyboards.main import get_main_kb

from lexicon import LEXICON

router = Router()


@router.message(F.text == 'Список отслеживаемых ссылок')
async def show_links(message: Message):
    data = pd.read_csv('../db/links.csv', delimiter=',', index_col=0)
    if len(data) == 0:
        await message.answer(LEXICON['empty_links'], reply_markup=get_main_kb())
    else:
        text = LEXICON['list_entry']
        for i, [header, url] in enumerate(zip(data['header'], data['url'])):
            text += f'{i + 1}\. [{header}]({url})\n'
        await message.answer(text, reply_markup=get_main_kb())
