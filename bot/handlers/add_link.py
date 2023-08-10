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


class NewLink(StatesGroup):
    pasting_new_link = State()
    heading = State()


@router.message(F.text == 'Отслеживать новую ссылку')
async def paste_new_link(message: Message, state: FSMContext):
    await message.answer(LEXICON['paste_new_link'], reply_markup=get_abort_kb())
    await state.set_state(NewLink.pasting_new_link)


@router.message(F.text == 'Отмена')
async def abort(message: Message, state: FSMContext):
    await message.answer(LEXICON['abort_new_link'], reply_markup=get_main_kb())
    await state.clear()


def check_link(link: str) -> str:
    if link.startswith('http'):  # and requests.get(link).status_code == 200:
        data = pd.read_csv('../db/links.csv', delimiter=',', index_col=0)
        if link in data['url'].values:
            return 'existing link'
        return 'good link'
    return 'bad link'


@router.message(NewLink.pasting_new_link, lambda message: check_link(message.text) == 'bad_link')
async def new_link_is_bad(message: Message):
    await message.answer(LEXICON['error_paste_new_link'])


@router.message(NewLink.pasting_new_link, lambda message: check_link(message.text) == 'existing link')
async def new_link_is_bad(message: Message):
    await message.answer(LEXICON['existing_link'])


@router.message(NewLink.pasting_new_link, lambda message: check_link(message.text) == 'good link')
async def new_link_is_good(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer(LEXICON['paste_new_heading'])
    await state.set_state(NewLink.heading)


def update_links(sample: dict) -> None:
    print(sample)

    data = pd.read_csv('../db/links.csv', delimiter=',', index_col=0)
    new_link = pd.DataFrame({'header': [sample['header']], 'url': [sample['url']]})
    upd_data = pd.concat([data, new_link])
    upd_data.to_csv('../db/links.csv')


@router.message(NewLink.heading)
async def paste_new_heading(message: Message, state: FSMContext):
    await state.update_data(header=message.text)
    sample = await state.get_data()
    update_links(sample)
    await state.clear()

    await message.answer(LEXICON['success_new_link'], reply_markup=get_main_kb())
