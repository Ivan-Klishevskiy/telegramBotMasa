from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from props import DISABLE_WORDS
from src.database.repositories.user_repo import UserRep
from main import dp
from src.database.repositories.request_repo import RequestRep


class ComplaintState(StatesGroup):
    waiting_for_user_text = State()
    deleting_request = State()


async def add_not_urgen_step1(message: types.Message):
    if not await UserRep.get_user_by_id(message.from_user.id):
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    await ComplaintState.waiting_for_user_text.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Отмена"]
    keyboard.add(*buttons)
    await message.answer("Введите текст обращения:", reply_markup=keyboard)


@dp.message_handler(state=ComplaintState.waiting_for_user_text)
async def add_not_urgent_step2(message: types.Message, state: FSMContext):
    user = await UserRep.get_user_by_id(message.from_user.id)
    if not user:
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    if message.text == "Отмена":
        await message.answer("обращение отменено")
        await state.finish()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if user[0] == 'madrih':
            buttons = ["Cрочные", "Не срочные", "Главное меню"]
        else:
            buttons = ["Срочно", "Не срочно", "Мои обращения", "Главное меню"]
        keyboard.add(*buttons)

        await message.answer("Выберите тип обращения:", reply_markup=keyboard)

        return

    if message.text in DISABLE_WORDS:
        await message.answer("Отказано, введено недоступное слово.\nВведите текст обращения:")
    else:

        user = await UserRep.get_user_by_id(message.from_user.id)

        await RequestRep.save_not_urgent_request(username=str(user[0]), message=message.text)
        await message.answer("Обращение успешно зарегистрировано\n"
                             "Для отправки еще одного обращения выберите тип обращения.\n"
                             "Для возарщения в главное меню нажмите 'Главная'")
        await state.finish()


async def add_urgen_step1(message: types.Message):
    if not await UserRep.get_user_by_id(message.from_user.id):
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    await ComplaintState.waiting_for_user_text.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Отмена"]
    keyboard.add(*buttons)
    await message.answer("Введите текст обращения:", reply_markup=keyboard)


@dp.message_handler(state=ComplaintState.waiting_for_user_text)
async def add_urgent_step2(message: types.Message, state: FSMContext):
    user = await UserRep.get_user_by_id(message.from_user.id)
    if not user:
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    if message.text == "Отмена":
        await message.answer("обращение отменено")
        await state.finish()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if user[0] == 'madrih':
            buttons = ["Cрочные", "Не срочные", "Главное меню"]
        else:
            buttons = ["Срочно", "Не срочно", "Мои обращения", "Главное меню"]
        keyboard.add(*buttons)

        await message.answer("Выберите тип обращения:", reply_markup=keyboard)

        return

    if message.text in DISABLE_WORDS:
        await message.answer("Отказано, введено недоступное слово.\nВведите текст обращения:")
    else:
        user = await UserRep.get_user_by_id(message.from_user.id)

        await RequestRep.save_urgent_request(username=str(user[0]), message=message.text)
        await message.answer("Обращение успешно зарегистрировано\n"
                             "Для отправки еще одного обращения выберите тип обращения\n"
                             "Для возарщения в главное меню нажмите 'Главная'")

        await state.finish()


async def show_requests(message: types.Message):
    user = await UserRep.get_user_by_id(message.from_user.id)
    username = str(user[0])
    urgent_requests, not_urgent_requests = await RequestRep.fetch_user_requests_by_username(username)
    if not urgent_requests and not not_urgent_requests:
        await message.answer("У вас нет обращений.")
        return

    for req in urgent_requests + not_urgent_requests:
        urgent = req in urgent_requests
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Отменить', callback_data=f'delete_request:{urgent}:{req[1]}'))
        await message.answer(f"{req[1]}", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('delete_request'))
async def process_callback(callback_query: types.CallbackQuery):
    user = await UserRep.get_user_by_id(callback_query.from_user.id)
    username = str(user[0])
    await callback_query.answer()
    _, urgent, message = callback_query.data.split(':', 2)
    await RequestRep.delete_request(username, message, urgent == 'True')
    await callback_query.message.edit_text("Обращение удалено.")
