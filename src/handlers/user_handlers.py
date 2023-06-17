from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

from props import DISABLE_WORDS
from src.handlers.main_handlers import show_main_options
from main import dp
from src.database.repositories.user_repo import UserRep


class ChoiceState(StatesGroup):
    waiting_for_choice = State()


class LoginState(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()


class RegisterState(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()


@dp.message_handler(Command('start'))
async def start_command(message: types.Message):
    telegram_id = message.from_user.id

    user = await UserRep.get_user_by_id(telegram_id)
    if user is not None:
        await message.answer(f'Привет, {user[0]}!')
        await show_main_options(message)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Войти", "Зарегистрироваться"]
        keyboard.add(*buttons)
        await ChoiceState.waiting_for_choice.set()
        await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.message_handler(state=ChoiceState.waiting_for_choice)
async def choice_start_menu(message: types.Message, state: FSMContext):
    if message.text.lower() == 'войти':
        await state.finish()
        await login_step1(message)
    if message.text.lower() == 'зарегистрироваться':
        await state.finish()
        await register_step1(message)


async def login_step1(message: types.Message):
    await LoginState.waiting_for_username.set()
    await message.answer("Введите логин:")


@dp.message_handler(state=LoginState.waiting_for_username)
async def login_step2(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await LoginState.next()
    await message.answer("Введите пароль:")


@dp.message_handler(state=LoginState.waiting_for_password)
async def login_step3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    password = message.text

    temp_user = await UserRep.get_user_by_login_pass(username, password)

    if temp_user:
        await UserRep.update_user(message.from_user.id, username, password)
        await message.answer("Вы успешно вошли в систему!")
        await show_main_options(message)
        await state.finish()
    else:
        await message.answer("Логин или пароль введены неверно.")
        await state.finish()
        await start_command(message)


async def register_step1(message: types.Message):
    await RegisterState.waiting_for_username.set()
    await message.answer("Введите логин:")


@dp.message_handler(state=RegisterState.waiting_for_username)
async def register_step2(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await RegisterState.next()
    await message.answer("Введите пароль:")


@dp.message_handler(state=RegisterState.waiting_for_password)
async def register_step3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    password = message.text

    if username in DISABLE_WORDS:
        await message.answer("Использовано недоступное слово.")
        await state.finish()
        await start_command(message)

    else:
        if await UserRep.get_user_by_username(username):
            await message.answer("Такой пользователь уже существует.")
            await state.finish()
            await start_command(message)
        else:
            await UserRep.registr_user(message.from_user.id, username, password)
            await message.answer("Вы успешно зарегистрировались!")
            await state.finish()
            await show_main_options(message)
