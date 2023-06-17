from aiogram import types
from src.database.repositories.user_repo import UserRep
from src.handlers.complaint_handlers import add_urgen_step1, add_not_urgen_step1, show_requests
from src.handlers.topic_handlers import show_topics, add_topic_step1
from main import dp


async def show_main_options(message: types.Message):
    if not await UserRep.get_user_by_id(message.from_user.id):
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Голосование", "Обращение"]
    keyboard.add(*buttons)
    await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ["Голосование", "Обращение"])
async def choice_main_option(message: types.Message):
    if not await UserRep.get_user_by_id(message.from_user.id):
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    if message.text == "Голосование":
        await show_topic_options(message)
    elif message.text == "Обращение":
        await show_request_options(message)


async def show_request_options(message: types.Message):
    if not await UserRep.get_user_by_id(message.from_user.id):
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Срочно", "Не срочно", "Мои обращения", "Главное меню"]
    keyboard.add(*buttons)

    await message.answer("Выберите тип обращения:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in ["Срочно", "Не срочно", "Мои обращения"])
async def choice_topic_options(message: types.Message):
    if not await UserRep.get_user_by_id(message.from_user.id):
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

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
