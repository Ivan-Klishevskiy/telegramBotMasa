from aiogram import types
from src.database.repositories.user_repo import UserRep
from src.handlers.complaint_handlers import add_urgen_step1, add_not_urgen_step1, show_requests
from src.handlers.madrih_handlers import show_not_urgent_requests, show_urgent_requests
from src.handlers.topic_handlers import show_topics, add_topic_step1
from main import dp, bot


async def show_main_options(message: types.Message):
    if not await UserRep.get_user_by_id(message.from_user.id):
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Голосование", "Обращение", "Выход"]
    keyboard.add(*buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ["Голосование", "Обращение", "Выход"])
async def choice_main_option(message: types.Message):
    if message.text == "Выход":
        await exit_user(message)
        return
    if not await UserRep.get_user_by_id(message.from_user.id):
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    if message.text == "Голосование":
        await show_topic_options(message)
    elif message.text == "Обращение":
        await show_request_options(message)


async def show_request_options(message: types.Message):
    user = await UserRep.get_user_by_id(message.from_user.id)
    if not user:
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    if user[0] == 'madrih':
        buttons = ["Cрочные", "Не срочные", "Главное меню"]
    else:
        buttons = ["Срочно", "Не срочно", "Мои обращения", "Главное меню"]
    keyboard.add(*buttons)

    await message.answer("Выберите тип обращения:", reply_markup=keyboard)


async def exit_user(message: types.Message):
    await UserRep.remove_telegram_id(message.from_user.id)
    await message.answer("Вы вышли из аккаунта.\nДля входа или регистрации нажмите на /start")


@dp.message_handler(lambda message: message.text in ["Cрочные", "Не срочные", "Срочно", "Не срочно", "Мои обращения"])
async def choice_topic_options(message: types.Message):
    user = await UserRep.get_user_by_id(message.from_user.id)
    if not user:
        await message.answer("Пожалуйста, авторизуйтесь.")
        return
    if user[0] == 'madrih':
        if message.text == "Cрочные":
            await show_urgent_requests(message)
        elif message.text == "Не срочные":
            await show_not_urgent_requests(message)
    else:
        if message.text == "Срочно":
            await add_urgen_step1(message)
        elif message.text == "Не срочно":
            await add_not_urgen_step1(message)
        elif message.text == "Мои обращения":
            await show_requests(message)


async def show_topic_options(message: types.Message):
    if not await UserRep.get_user_by_id(message.from_user.id):
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Показать все темы", "Добавить новую тему", "Главное меню"]
    keyboard.add(*buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ["Показать все темы", "Добавить новую тему", "Главное меню"])
async def choice_topic_options(message: types.Message):
    if not await UserRep.get_user_by_id(message.from_user.id):
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    if message.text == 'Показать все темы':
        await show_topics(message)
    elif message.text == 'Добавить новую тему':
        await add_topic_step1(message)
    elif message.text == 'Главное меню':
        await show_main_options(message)
