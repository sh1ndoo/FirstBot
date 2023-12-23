from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from requests import get

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN = '6894279538:AAEqmWRysUGEytsUuGa_B7g-Jm1YxQycCgQ'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )

@dp.message(Command(commands=['check_prem']))
async def process_prem(message):
    if get('https://api.telegram.org/bot6894279538:AAEqmWRysUGEytsUuGa_B7g-Jm1YxQycCgQ/getUpdates?offset=-1').json()['result'][0]['message']['from']['is_premium']:
        await message.answer('123')


@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)