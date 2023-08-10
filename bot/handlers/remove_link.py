import pandas as pd
import requests
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from lexicon import LEXICON
from keyboards.abort import get_abort_kb
from keyboards.main import get_main_kb


router = Router()


class RemoveLink(StatesGroup):
    checking_number = State()


@router.message(F.text == 'Удалить ссылку из отслеживаемых')
async def paste_new_link(message: Message, state: FSMContext):
    data = pd.read_csv('../db/links.csv', delimiter=',', index_col=0)
    if len(data) == 0:
        await message.answer(LEXICON['empty_links'], reply_markup=get_main_kb())
    else:
        text = LEXICON['list_entry']
        for i, [header, url] in enumerate(zip(data['header'], data['url'])):
            text += f'{i + 1}\. [{header}]({url})\n'
        await message.answer(text, reply_markup=get_abort_kb())

    await message.answer(LEXICON['number_remove_link'])
    await state.set_state(RemoveLink.checking_number)


@router.message(F.text == 'Отмена')
async def abort(message: Message, state: FSMContext):
    await message.answer(LEXICON['abort_new_link'], reply_markup=get_main_kb())
    await state.clear()


@router.message(RemoveLink.checking_number, lambda message: not message.text.isdigit())
async def bad_number(message: Message):
    await message.answer(LEXICON['bad_number'])


@router.message(RemoveLink.checking_number, lambda message: message.text.isdigit())
async def good_number(message: Message, state: FSMContext):
    idx = int(message.text) - 1
    goal_header = ''
    data = pd.read_csv('../db/links.csv', delimiter=',', index_col=0)

    for i, header in enumerate(data['header']):
        if i == idx:
            goal_header = header
            break

    if not goal_header:
        await message.answer(LEXICON['not_existing_number'])
    else:
        upd_data = data[data['header'] != goal_header]
        upd_data.to_csv('../db/links.csv')
        await message.answer(LEXICON['success_remove_link'], reply_markup=get_main_kb())
        await state.clear()
