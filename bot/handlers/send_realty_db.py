import pandas as pd
from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from bot.keyboards.main import get_main_kb
from bot.lexicon import LEXICON
from bot.utils import clean_str, BUTTONS, REALTY_COLUMNS, LINKS_FILEPATH
from parsers.avito import get_new_offers

router = Router()


@router.message(F.text == BUTTONS['send_realty_db'])
async def send_realty_db(message: Message):
    links = pd.read_csv(LINKS_FILEPATH, delimiter=',', index_col=0)

    if len(links) != 1:
        mess = clean_str(LEXICON['not_one_link'])
        await message.answer(mess, reply_markup=get_main_kb())
    else:
        mess = clean_str(LEXICON['loading_realty'])
        await message.answer(mess)

        url: str = links['url'][0]
        export_df = pd.DataFrame(columns=REALTY_COLUMNS)

        for page in range(1, 101):
            print(page)
            raw_offers = get_new_offers(url + f'&p={page}', update_db=False)
            if not raw_offers:
                break
            values_list = [d.values() for d in raw_offers]
            export_df = pd.concat([export_df, pd.DataFrame(values_list, columns=REALTY_COLUMNS)])


        export_df.to_excel('bot/files/realty_database.xlsx')

        file = FSInputFile('bot/files/realty_database.xlsx')
        await message.answer_document(file)
