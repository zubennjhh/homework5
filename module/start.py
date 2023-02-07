from aiogram import types
from module.constans import START_TEXT
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

""" Обработчик категорий """
start_kb = InlineKeyboardMarkup(resize_keyboard=True)
start_kb.add(
	InlineKeyboardButton('Анкета', callback_data='form_start'),
	InlineKeyboardButton('Помощь', callback_data='help_command')
)


async def start_command(message: types.Message):
	"""
		Функция приветствия пользовователя
	"""
	await message.answer(text=START_TEXT.format(first_name=message.from_user.first_name), reply_markup=start_kb)
	await message.delete()
