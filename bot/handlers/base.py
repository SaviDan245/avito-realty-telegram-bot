from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Welcome to Echobot\!')


# @router.message(F.text)
# async def echo_message(message: Message):
#     await message.answer(message.text)
