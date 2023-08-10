from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()

    kb.button(text='Список отслеживаемых ссылок')
    kb.button(text='Отслеживать новую ссылку')
    kb.button(text='Удалить ссылку из отслеживаемых')
    kb.button(text='Скачать базу данных')
    kb.button(text='Изменить частоту уведомлений')

    kb.adjust(1, 1, 1, 1, 1)

    return kb.as_markup(resize_keyboard=True)
