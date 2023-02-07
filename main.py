from aiogram import types, executor
from aiogram.dispatcher.filters import Text
import logging
from config import dp
from module.start import start_command
from module.help import help_command
from module.fsm import (
    Form,
    cancel_handler,
    form_start,
    name_command,
    remind_command,
    time_command,
    done_command,
    napominalka,
    scheduler
)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)


    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(form_start, commands=['form'])
    dp.register_message_handler(form_start, commands=['napominalka'])
    dp.register_message_handler(form_start, Text(equals='Нет'), state=Form.done)
    dp.register_message_handler(cancel_handler, state='*', commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(name_command, state=Form.name)
    dp.register_message_handler(remind_command, state=Form.remind)
    dp.register_message_handler(time_command, state=Form.time)
    dp.register_message_handler(done_command, Text(equals='Да'), state=Form.done)
    dp.register_message_handler(napominalka, Text(equals='start'), state=Form.start_re)
    dp.register_message_handler(scheduler, commands="start")

    executor.start_polling(dp, skip_updates=True)
