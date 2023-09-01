import asyncio
import logging

from aiocron import crontab
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from src.config import REDIS_STATE_DB_NUMBER, NOTIFICATION_MINUTES, bot
from src.handlers import register_handlers
from src.utils.task import schedule_task

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    # filename='logs.log'
)


async def on_startup():
    await schedule_task()


async def main():
    storage = RedisStorage2(db=REDIS_STATE_DB_NUMBER)
    dp = Dispatcher(bot, storage=storage)

    register_handlers(dp)

    crontab(f'*/{NOTIFICATION_MINUTES} * * * *', func=schedule_task)

    try:
        await dp.skip_updates()
        await on_startup()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        session = await bot.get_session()
        await session.close()


if __name__ == '__main__':
    asyncio.run(main())
