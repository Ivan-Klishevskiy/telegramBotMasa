from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

import config
from background import keep_alive

from src.database.db_init import create_db
from src.tools.utils import install_script_dependencies

bot = Bot(token=config.TELEGRAM_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())

from src.handlers.user_handlers import *

keep_alive()
if __name__ == '__main__':
    # install_script_dependencies()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
    from aiogram import executor

    executor.start_polling(dp)
