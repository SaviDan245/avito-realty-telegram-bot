import asyncio
from datetime import datetime

import pandas as pd
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from bot.keyboards.main import get_main_kb
from bot.keyboards.stop_track import get_stop_kb
from bot.lexicon import LEXICON
from bot.utils import BUTTONS, LINKS_FILEPATH, N_TILDAS, clean_str, parse_offers, get_freq
from parsers.avito import get_new_offers_by_driver

router = Router()


class Tracker(StatesGroup):
    running = State()
    stop = State()


@router.message(F.text == BUTTONS['begin_tracking'])
async def begin_tracking(message: Message, state: FSMContext):
    links = pd.read_csv(LINKS_FILEPATH, delimiter=',', index_col=0)
    if len(links) == 0:
        mess = clean_str(LEXICON['empty_links'])
        await message.answer(mess, reply_markup=get_main_kb())
    else:
        await state.set_state(Tracker.running)
        mess = clean_str(LEXICON['begin_tracking'])
        await message.answer(mess, reply_markup=get_stop_kb())
        while True:
            status = await state.get_state()
            if status == 'Tracker:running':
                service = Service(executable_path=GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service)
                
                for i, [header, url] in enumerate(zip(links['header'], links['url'])):
                    driver.get(url)
                    raw_offers = get_new_offers_by_driver(driver, message.from_user.id)
                    new_offers = parse_offers(raw_offers)
                    if not new_offers:
                        print('No new offers')
                        continue
                    else:
                        # header_mess = clean_str(f'*Ссылка №{i + 1}. [{header}]({url})*\n\n' + r'\~' * N_TILDAS + '\n\n')
                        # await message.answer(header_mess)
                        for text in new_offers:
                            htext = f'__*От ссылки: {header}*__\n\n' + r'\~' * N_TILDAS + '\n\n' + text
                            mess = clean_str(htext)
                            await message.answer(mess)
                
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                print(f"Tracked for {message.from_user.username}: ", dt_string)
                driver.quit()
                await asyncio.sleep(get_freq())


@router.message(F.text == BUTTONS['stop_tracking'])
async def stop_tracking(message: Message, state: FSMContext):
    await state.set_state(Tracker.stop)
    mess = clean_str(LEXICON['stop_tracking'])
    await message.answer(mess, reply_markup=get_main_kb())
