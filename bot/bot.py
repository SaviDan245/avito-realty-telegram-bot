import asyncio

from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import base, list_links, add_link


# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='MarkdownV2')
    dp = Dispatcher()
    dp.include_routers(base.router, list_links.router, add_link.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
