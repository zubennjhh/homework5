from aiogram import types
from module.constans import HELP_TEXT


async def help_command(message: types.Message):
    """
        Фунция для просмотра списка доступных команд
    """

    await message.answer(text=HELP_TEXT)
    await message.delete()
