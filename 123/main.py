from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from random import randint
from requests import get

BOT_TOKEN = '6976134083:AAEGZcK6QlmN9nQecOjIX66I71RlC32BzV4'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

users = {}


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}
    await message.answer('Помогите, надо мной ставят опыты...')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Тебе уже никто не поможет...'
    )


@dp.message(Command(commands=['check_prem']))
async def process_prem(message: Message):
    if message.from_user.is_premium:
        await message.answer(f'Жесть богатый')
    else:
        await message.answer('Жесть не богатый')


@dp.message(Command(commands='play_game'))
async def playing_bin_game(message: Message):
    await message.answer('Хорошо, давай поиграем... Попробуй отгадать загаданное мной число от 1 до 100, иначе...')
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
            await message.answer('Человек оказался умнее меня...')
        elif int(message.text) > users[id]['secret_number']:
            users[id]['attempts'] -= 1
            await message.answer(f'Мое число меньше\nУ тебя осталось всего {users[id]['attempts']} попыток...')
        elif int(message.text) < users[id]['secret_number']:
            users[id]['attempts'] -= 1
            await message.answer(f'Мое число больше\nУ тебя осталось всего {users[id]['attempts']} попыток...')

        if users[id]['attempts'] == 0:
            users[id]['in_game'] = False
            users[id]['total_games'] += 1
            await message.answer(f'Ха-ха, я умнее тебя, у меня памяти {users[id]['secret_number']} мегабайт')
    else:
        await send_echo(message)


@dp.message(Command(commands='bin_game_stat'))
async def statistic(message: Message):
    id = message.from_user.id
    await message.answer(f'''
    Побед: {users[id]['wins']}
Всего игр: {users[id]['total_games']}
Процент побед: {users[id]['wins'] / users[id]['total_games'] * 100 if users[id]['wins'] > 0 else 0}%''')


@dp.message(Command(commands='cancel'))
async def cancelling(message: Message):
    id = message.from_user.id
    if users[id]['in_game']:
        await message.answer(f'Ха-ха, я умнее тебя, у меня памяти {users[id]['attempts']} мегабайт!')
    else:
        await send_echo(message)


@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )


if __name__ == '__main__':
    dp.run_polling(bot)
