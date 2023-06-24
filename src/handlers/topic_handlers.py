from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from props import DISABLE_WORDS
from src.database.repositories.user_repo import UserRep
from src.database.repositories.topic_repo import TopicRep
from main import dp, bot


class TopicState(StatesGroup):
    waiting_for_topic = State()


async def show_topics(message: types.Message):
    user = await UserRep.get_user_by_id(message.from_user.id)
    if not user:
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    topics = await TopicRep.get_all_topics()

    if topics:
        for topic in topics:
            keyboard = types.InlineKeyboardMarkup()

            if user[0] == 'madrih':
                button = types.InlineKeyboardButton(text="Удалить", callback_data=f"delete_{topic[0]}")
                keyboard.add(button)
            else:
                button = types.InlineKeyboardButton(text="Голосовать", callback_data=f"vote_{topic[0]}")
                keyboard.add(button)
            last_name = await UserRep.get_user_info_by_username(topic[1])
            await message.answer(f"От {last_name[0]}\n{topic[2]} (голосов: {topic[3]})", reply_markup=keyboard)

        await message.answer('Проголосуйте за тему которая вам интересна'
                             ' или предложите новую нажав на кнопку "Добавить новую тему"')
    else:
        await message.answer('Список тем пуст. Самое время добавить новую тему.'
                             ' Для этого выберите кнопку "Добавить новую тему"')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('vote_'))
async def process_callback(callback_query: types.CallbackQuery):
    topic_id = int(callback_query.data.split('_')[1])

    if await TopicRep.check_user_voted(callback_query.from_user.id, topic_id):
        await bot.answer_callback_query(callback_query.id, "Вы уже проголосовали за эту тему!")
        return

    await TopicRep.update_topic_count_voice(topic_id)
    await TopicRep.create_voice(callback_query.from_user.id, topic_id)

    await bot.answer_callback_query(callback_query.id, "Вы проголосовали!")


async def add_topic_step1(message: types.Message):
    if not await UserRep.get_user_by_id(message.from_user.id):
        await message.answer("Пожалуйста, авторизуйтесь.")
        return

    await TopicState.waiting_for_topic.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Отмена"]
    keyboard.add(*buttons)
    await message.answer("Введите тему:", reply_markup=keyboard)


@dp.message_handler(state=TopicState.waiting_for_topic)
async def add_topic_step2(message: types.Message, state: FSMContext):
    user = await UserRep.get_user_by_id(message.from_user.id)
    if not user:
        await message.answer("Пожалуйста, авторизуйтесь.")
        return
    if message.text == "Отмена":
        await message.answer("Добавление темы отменено")
        await state.finish()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Показать все темы", "Добавить новую тему", "Главное меню"]
        keyboard.add(*buttons)
        await message.answer("Выберите действие:", reply_markup=keyboard)
        return
    if message.text in DISABLE_WORDS:
        await message.answer("Отказано, введено недоступное слово.\nВведите тему:")
    else:
        await TopicRep.create_topic(user[0], message.text)
        await message.answer("Тема успешно добавлена.")
        await state.finish()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Показать все темы", "Добавить новую тему", "Главное меню"]
        keyboard.add(*buttons)
        await message.answer("Выберите действие:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('delete_'))
async def process_delete_callback(callback_query: types.CallbackQuery):
    topic_id = int(callback_query.data.split('_')[1])

    await TopicRep.delete_topic(topic_id)

    await bot.answer_callback_query(callback_query.id, "Тема успешно удалена.")
