import requests
from pprint import pprint
import time

API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '6894279538:AAEqmWRysUGEytsUuGa_B7g-Jm1YxQycCgQ'
TEXT = 'c премиумом? Богатый чтоле? Котика тогда не будет'
TEXT_2 = 'Нет денег на прем:( Ну держи тогда котика хотя бы'
MAX_COUNTER = 500


API_CAT = 'https://api.thecatapi.com/v1/images/search'

offset = -2
counter = 0
chat_id: int


while counter < MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            name = result['message']['from']['first_name']
            if result['message']['from']['is_premium']:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={', '.join((name, TEXT_2))}')
                cat = requests.get(API_CAT).json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat}')
                print(name)
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={' '.join((name, TEXT_2))}')
                cat = requests.get(API_CAT).json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat}')

    time.sleep(1)
    counter += 1
