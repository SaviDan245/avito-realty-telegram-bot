from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import pandas as pd
import requests

from keyboards.main import get_main_kb
from lexicon import LEXICON

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(LEXICON['/start'], reply_markup=get_main_kb())


# @router.message(F.text == 'привет')
# async def cmd_hello(message: Message):
#     await message.reply('Пошёл нахуй\!\n\n\nДа, ты\.')


@router.message(F.text == 'Список отслеживаемых ссылок')  # TODO: добавить "ссылки отсутствуют"
async def show_links(message: Message):
    data = pd.read_csv('../db/links.csv', delimiter=',')
    text = LEXICON['list_entry']
    for i, [header, url] in enumerate(zip(data['header'], data['url'])):
        text += f'{i + 1}\. [{header}]({url})\n'

    await message.answer(text, reply_markup=get_main_kb())


class NewLink(StatesGroup):
    pasting_new_link = State()
    heading = State()
    fuck_you = State()


@router.message(F.text == 'Отслеживать новую ссылку')
async def paste_new_link(message: Message, state: FSMContext):
    await message.answer(LEXICON['paste_new_link'])
    await state.set_state(NewLink.pasting_new_link)


def check_link(link: str) -> bool:  # TODO: добавить проверку на уникальность ссылки
    # if link.startswith('http'):
    #     return requests.get(link).status_code == 200
    return link.startswith('http')


@router.message(NewLink.pasting_new_link, lambda message: not check_link(message.text))
async def new_link_is_bad(message: Message):
    await message.answer(LEXICON['error_paste_new_link'])


@router.message(NewLink.pasting_new_link, lambda message: check_link(message.text))
async def new_link_is_good(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer(LEXICON['paste_new_heading'])
    await state.set_state(NewLink.heading)


@router.message(NewLink.heading)
async def paste_new_heading(message: Message, state: FSMContext):
    await state.update_data(header=message.text)
    await state.set_state(NewLink.fuck_you)

    # sample = await state.get_data()
    #
    # print(sample)
    #
    # data = pd.read_csv('../db/links.csv', delimiter=',', index_col=0)
    # new_link = pd.DataFrame({'header': [sample['header']], 'url': [sample['url']]})
    # upd_data = pd.concat([data, new_link])
    # upd_data.to_csv('../db/links.csv')
    #
    # await state.clear()


@router.message(NewLink.fuck_you)
async def add_new_link(state: FSMContext):
    sample = await state.get_data()

    print('HERE')

    data = pd.read_csv('../db/links.csv', delimiter=',', index_col=0)
    new_link = pd.DataFrame({'header': sample['header'], 'url': sample[url]})
    upd_data = pd.concat([data, new_link])
    upd_data.to_csv('../db/links.csv')

    await state.clear()
