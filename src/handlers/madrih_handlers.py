from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from main import dp
from src.database.repositories.request_repo import RequestRep
from src.database.repositories.user_repo import UserRep


async def show_not_urgent_requests(message: types.Message):
    not_urgent_requests = await RequestRep.get_all_not_urgent_requests()
    if not not_urgent_requests:
        await message.answer("У вас нет не срочных обращений.")
        return

    for req in not_urgent_requests:
        urgent = req in not_urgent_requests
        keyboard = InlineKeyboardMarkup()
        user_info = await UserRep.get_user_info_by_username(req[0])
        keyboard.add(InlineKeyboardButton('Удалить', callback_data=f'delete_request:{urgent}:{req[1]}'))
        await message.answer(f"{user_info[0]}\nкв:{user_info[1]}\n{req[1]}", reply_markup=keyboard)


async def show_urgent_requests(message: types.Message):
    not_urgent_requests = await RequestRep.get_all_urgent_requests()
    if not not_urgent_requests:
        await message.answer("У вас нет срочных обращений.")
        return

    for req in not_urgent_requests:
        urgent = req in not_urgent_requests
        keyboard = InlineKeyboardMarkup()
        user_info = await UserRep.get_user_info_by_username(req[0])
        keyboard.add(InlineKeyboardButton('Удалить', callback_data=f'delete_request_madrih:{urgent}:{req[1]}'))
        await message.answer(f"{user_info[0]}\nкв:{user_info[1]}\n{req[1]}", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('delete_request_madrih'))
async def process_callback(callback_query: types.CallbackQuery):
    user = await UserRep.get_user_by_id(callback_query.from_user.id)
    username = str(user[0])
    if username == 'madrih':
        await callback_query.answer()
        _, urgent, message = callback_query.data.split(':', 2)
        await RequestRep.delete_request_madrih(message, urgent == 'True')
        await callback_query.message.edit_text("Обращение удалено.")
