import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import base, list_links, add_link, remove_link

logger = logging.getLogger(__name__)


# Запуск бота
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')

    bot = Bot(token=config.bot_token.get_secret_value(),
              parse_mode='MarkdownV2')
    dp = Dispatcher()

    dp.include_router(base.router)
    dp.include_router(add_link.router)
    dp.include_router(list_links.router)
    dp.include_router(remove_link.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
