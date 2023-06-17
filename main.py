from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

from src.database.db_init import create_db
from src.tools.utils import install_script_dependencies

bot = Bot(token='6218030678:AAHChCLNmQw8Kl4Vj_JikuMFKG3EqS4ppyU')
dp = Dispatcher(bot, storage=MemoryStorage())

from src.handlers.user_handlers import *

if __name__ == '__main__':
    # install_script_dependencies()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
    from aiogram import executor

    executor.start_polling(dp)
