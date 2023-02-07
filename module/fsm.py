import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import aioschedule
from config import bot
from aiogram import types


class Form(StatesGroup):
    name = State()
    remind = State()
    time = State()
    done = State()
    start_re = State()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply(
        'Отмена',
        reply_markup=types.ReplyKeyboardRemove())


async def form_start(message: types.Message):
    """
        Функция для старта нашего FSM и задаем первый вопрос
    """
    await Form.name.set()
    await message.reply("Введите ваше имя:")


async def name_command(message: types.Message, state: FSMContext):
    """
        Обрабатываем имя и задаем второй вопрос
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Что вам нужно напомнить?")


async def remind_command(message: types.Message, state: FSMContext):
    '''
        Обрабатываем второй вопрос и задаем третий вопрос
    '''
    async with state.proxy() as data:
        data['remind'] = message.text

    await Form.next()
    await message.reply("Во сколько вам нужно напомнить? (Например: 7:30)")


async def time_command(message: types.Message, state: FSMContext):
    '''
        Обрабатываем третий вопрос
    '''
    async with state.proxy() as data:
        data['time'] = message.text

    yes_no_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    yes_no_kb.add(
        KeyboardButton("Да"),
        KeyboardButton("Нет")
    )

    await Form.next()
    await message.reply(f"""Подтвердите ваши данные:
        Имя: {data['name']}
        Вам нужно напомнить: {data['remind']}
        Время в которое будет напоминание: {data['time']}
        Данные верны?
        """, reply_markup=yes_no_kb)


async def done_command(message: types.Message, state: FSMContext):

    await state.finish()
    await message.reply(
        "Я надеюсь я был полезен вам, для начало отсчета пропишите - start",
        reply_markup=start_re)

start_re = ReplyKeyboardMarkup(resize_keyboard=True)
start_re.add(
    KeyboardButton("start")
    )


async def napominalka(message: types.Message):
    '''
        Функция напоминания
    '''

    await bot.send_message(
        chat_id=message.from_user.id,
        text=f'''Привет еще раз {data['name']}! Ты не забыл - {data['remind']}?''',
    )


async def scheduler():
    aioschedule.every().day.at(time_command).do(napominalka)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
