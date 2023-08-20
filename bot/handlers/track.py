import asyncio

import pandas as pd
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot.keyboards.main import get_main_kb
from bot.lexicon import LEXICON
from bot.utils import BUTTONS, TRACK_FREQ_FILEPATH, LINKS_FILEPATH, N_TILDAS, clean_str, parse_offers
from parsers.avito import get_new_offers

router = Router()


class Tracker(StatesGroup):
    running = State()
    stop = State()


@router.message(F.text == BUTTONS['begin_tracking'])
async def begin_tracking(message: Message, state: FSMContext):
    with open(TRACK_FREQ_FILEPATH) as f:
        freq = int(f.readline().strip())

    data = pd.read_csv(LINKS_FILEPATH, delimiter=',', index_col=0)
    if len(data) == 0:
        mess = clean_str(LEXICON['empty_links'])
        await message.answer(mess, reply_markup=get_main_kb())
    else:
        await state.set_state(Tracker.running)
        mess = clean_str(LEXICON['begin_tracking'])
        await message.answer(mess)
        while True:
            status = await state.get_state()
            if status == 'Tracker:running':
                for i, [header, url] in enumerate(zip(data['header'], data['url'])):
                    raw_offers = get_new_offers(url)
                    new_offers = parse_offers(raw_offers)
                    if not new_offers:
                        continue
                    else:
                        # header_mess = clean_str(f'*Ссылка №{i + 1}. [{header}]({url})*\n\n' + r'\~' * N_TILDAS + '\n\n')
                        # await message.answer(header_mess)
                        for text in new_offers:
                            htext = f'__*От ссылки: {header}*__\n\n' + r'\~' * N_TILDAS + '\n\n' + text
                            mess = clean_str(htext)
                            await message.answer(mess)
                await asyncio.sleep(freq)


@router.message(F.text == BUTTONS['stop_tracking'])
async def stop_tracking(message: Message, state: FSMContext):
    await state.set_state(Tracker.stop)
    mess = clean_str(LEXICON['stop_tracking'])
    await message.answer(mess)
