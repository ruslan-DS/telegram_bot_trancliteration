import os
import logging
import asyncio
from string import punctuation
from aiogram import Dispatcher, types, Bot
from aiogram.filters.command import Command
# from config import TOKEN


NATIONAL_LET = list('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
INTERNATIONAL_LET = ['A', 'B', 'V', 'G', 'D', 'E', 'E', 'ZH', 'Z', 'I', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', \
                     'F', 'KH', 'TS', 'CH', 'SH', 'SHCH', 'Y', 'IE', 'E', 'IU', 'IA']


logging.basicConfig(level=logging.INFO, filename='py_logis.log', filemode='w')

TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def greeting(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    logging.info(f'User {user_name} with such a custom ID - {user_id} sent message: {message.text}')
    await message.answer(f'Здравствуйте, {user_name}. Надеюсь этот бот поможет вам в решении вашей задачи :) \n'
                         f'Отправьте в следующем сообщении текст, который хотите преобразовать в формат латиницы.')

@dp.message()
async def translet(message: types.Message):
    user_id = message.from_user.id
    text_from_user = message.text

    # Очистим текст в случае некорректных данных, введеных пользователем
    for letter in text_from_user:
        if letter in punctuation and letter != ' ':
            logging.info(f'User with such custom ID - {user_id} introduced character - {letter}, that incorrect in our program.')
            text_from_user = text_from_user.replace(letter, '')

    # Проведем проверку в случае если пользователь ввел цифры
    if text_from_user.isdigit():
        logging.info(f'User with such custom ID - {user_id} introduced incorrect data.')
        await message.answer(f'Проверьте корректность введенных данных на отсутствие цифр и повторите попытку :)')

    # Создадим основной алгоритм преобразования текста
    for letter in text_from_user[:]:
        if letter != ' ':
            text_from_user = text_from_user.replace(letter, INTERNATIONAL_LET[NATIONAL_LET.index(letter.upper())])
    text_from_user = text_from_user.title()

    logging.info(f'User with such custom ID - {user_id} did to transliterate original text {message.text} on {text_from_user}')
    await message.answer(text_from_user)

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())