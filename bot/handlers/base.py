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
