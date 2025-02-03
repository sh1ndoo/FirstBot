import io
import sqlite3
from random import randint
import requests
from AI.text_to_image.sdxl import sdxl
import base64
from kb import main_keyboard, bin_inline_kb, img_inline_kb
from AI.text_to_text.gpt import gpt, trim_history, image_gen
from processing.commands import *

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, Message)

BOT_TOKEN = '6976134083:AAEGZcK6QlmN9nQecOjIX66I71RlC32BzV4'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

storage = MemoryStorage()

class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    gpt = State()        # Состояние ожидания ввода имени
    deepseek = State()         # Состояние ожидания ввода возраста
    sdxl = State()      # Состояние ожидания выбора пола
    mj = State()     # Состояние ожидания загрузки фото
    dall_e = State()   # Состояние ожидания выбора образования
    bin_game = State()   # Состояние ожидания выбора получать ли новости



# Этот хэндлер будет срабатывать на коллбэк "cancel"
@dp.callback_query(lambda c: c.data == 'cancel')
async def process_callback_button1(callback_query: CallbackQuery):
    id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    if users[id]['in_game']:
        users[id]['in_game'] = False
        await bot.send_message(id, f'Ха-ха, я умнее тебя, у меня памяти {users[id]['secret_number']} мегабайт!')


# Этот хэндлер будет срабатывать на коллбэк выбора модели
@dp.callback_query(lambda c: c.data in ['dall-e-3', 'midjourney', 'flux-realism', 'flux-anime', 'flux', 'sdxl'])
async def process_callback_img(callback_query: CallbackQuery):
    id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    users[id]['img_model'] = callback_query.data
    await callback_query.answer('Модель выбрана')



# Этот хэндлер будет срабатывать на сообщение "GPT"
@dp.message(lambda x: x.text == 'GPT')
async def gpt_swap(message: Message):
    users[message.from_user.id]['chat_gpt'] = not users[message.from_user.id]['chat_gpt']
    if users[message.from_user.id]['chat_gpt']:
        await message.answer('GPT включен')
    else:
        users[message.from_user.id]['gpt_story'] = []
        await message.answer('GPT выключен, история очищена')


# Этот хэндлер будет срабатывать на сообщение "Image Generator"
@dp.message(lambda x: x.text == 'Image Generator')
async def img_gen_mode_swap(message: Message):
    users[message.from_user.id]['image_gen'] = not users[message.from_user.id]['image_gen']
    if users[message.from_user.id]['image_gen']:
        await message.answer('''Генерация изображений включена
Выберите модель''', reply_markup=img_inline_kb)
    else:
        await message.answer('Генерация изображений отключена')

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Тебе уже никто не поможет...'
    )


# Этот хэндлер будет срабатывать на сообщение "Бинарный поиск"
@dp.message(lambda x: x.text == 'Бинарный поиск')
async def playing_bin_game(message: Message):
    await message.answer('Хорошо, давай поиграем... Попробуй отгадать загаданное мной число от 1 до 100', reply_markup=bin_inline_kb)
    users[message.from_user.id]['secret_number'] = randint(1, 100)
    users[message.from_user.id]['in_game'] = True
    users[message.from_user.id]['attempts'] = 5


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def playing_game(message: Message):
    id = message.from_user.id
    if users[id]['in_game']:
        print(users[id]['secret_number'])
        if int(message.text) == users[id]['secret_number']:
            users[id]['in_game'] = False
            users[id]['total_games'] += 1
            users[id]['wins'] += 1
            users[id]['percent_bin_wins'] = users[id]['wins'] / users[id]['total_games'] * 100
            await message.answer('Человек оказался умнее меня...')
        elif int(message.text) > users[id]['secret_number']:
            users[id]['attempts'] -= 1
            await message.answer(f'Мое число меньше\nУ тебя осталось всего {users[id]['attempts']} попыток...', reply_markup=bin_inline_kb)
        elif int(message.text) < users[id]['secret_number']:
            users[id]['attempts'] -= 1
            await message.answer(f'Мое число больше\nУ тебя осталось всего {users[id]['attempts']} попыток...', reply_markup=bin_inline_kb)

        if users[id]['attempts'] == 0:
            users[id]['in_game'] = False
            users[id]['total_games'] += 1
            users[id]['percent_bin_wins'] = users[id]['wins'] / users[id]['total_games'] * 100 if users[id]['wins'] > 0 else 0
            await message.answer(f'Ха-ха, я умнее тебя, у меня памяти {users[id]['secret_number']} мегабайт')
    else:
        await message.send_echo(message)


# Этот хэндлер будет срабатывать на сообщение "Игры👾"
@dp.message(lambda x: x.text == 'Игры👾')
async def statistic(message: Message):
    id = message.from_user.id
    await message.answer(f'''
    Бинарный поиск:
Побед: {users[id]['wins']}
Всего игр: {users[id]['total_games']}
Процент побед: {users[id]['wins'] / users[id]['total_games'] * 100 if users[id]['wins'] > 0 else 0}%''')


@dp.message()
async def send_gpt(message: Message):
    if users[message.from_user.id]['chat_gpt'] and not users[message.from_user.id]['image_gen']:
        image = None
        if message.photo:
            file_info = await bot.get_file(file_id=message.photo[-1].file_id)
            file_path = file_info.file_path
            file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            print(file_url)
            image = requests.get(file_url, stream=True).raw
            users[message.from_user.id]['gpt_story'].append({'role': 'user', 'content': message.caption if message.caption else '.'})
        else:
            users[message.from_user.id]['gpt_story'].append({'role': 'user', 'content': message.text})
        response = await gpt(users[message.from_user.id]['gpt_story'], image)
        users[message.from_user.id]['gpt_story'].append({'role': 'assistant', 'content': response.choices[0].message.content})
        users[message.from_user.id]['gpt_story'] = trim_history(users[message.from_user.id]['gpt_story'])
        print(users[message.from_user.id]['gpt_story'])
        await message.answer(response.choices[0].message.content)
    elif not users[message.from_user.id]['chat_gpt'] and users[message.from_user.id]['image_gen']:
        if users[message.from_user.id]['img_model'] in ['sdxl-3d', 'sdxl-anime', 'sdxl-cinematic', 'sdxl-photo', 'sdxl-pixel', 'sdxl']:
            response = await sdxl(message.text)
            img_bytes = base64.b64decode(response[0].split(',')[1])
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            data = {'chat_id': message.chat.id}
            files = {'photo': io.BytesIO(img_bytes)}
            response_tg = requests.post(url, data=data, files=files)
            response_tg.raise_for_status()
            print(response_tg.json())
        else:
            response = await image_gen(message.text, users[message.from_user.id]['img_model'])
            image_url = response.data[0].url
            print(image_url)
            await message.answer_photo(image_url)
    else:
        await message.send_copy(chat_id=message.chat.id)

# dp.message.register(process_start_command, CommandStart(), StateFilter(default_state))
# dp.message.register(information, lambda x: x.text == 'Информация📝', StateFilter(default_state))
# dp.message.register(links, lambda x: x.text == 'Полезные ссылки🔗', StateFilter(default_state))



if __name__ == '__main__':
    dp.run_polling(bot)
