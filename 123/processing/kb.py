from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb = [
    [
        KeyboardButton(text="Информация📝"),
        KeyboardButton(text="Полезные ссылки🔗"),
    ],
    [
        KeyboardButton(text="Полезные инструменты⚒️"),
    ],
    [
        KeyboardButton(text="Игры👾"),
    ],
    [
        KeyboardButton(text="Нейронки"),
    ],
]
main_keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

urlButton = InlineKeyboardButton(text='Отменить игру', callback_data='cancel')
bin_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                    [
                                                        urlButton
                                                    ]
                                                     ])


urlButton_img1 = InlineKeyboardButton(text='DALL-E 3', callback_data='dall-e-3')
urlButton_img2 = InlineKeyboardButton(text='Midjourney', callback_data='midjourney')
urlButton_img3 = InlineKeyboardButton(text='SDXL', callback_data='sdxl')
urlButton_img4 = InlineKeyboardButton(text='NSFW', callback_data='nsfw')


img_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                    [
                                                        urlButton_img1,
                                                        urlButton_img2,
                                                        urlButton_img3,
                                                        urlButton_img4,
                                                    ],
                                                     ])

# [
#     KeyboardButton(text="Импорт тг-тг"),
#     KeyboardButton(text="Сообщения -> текст"),
#     KeyboardButton(text="?"),
# ],
#
# [
#     KeyboardButton(text="Бинарный поиск"),
#     KeyboardButton(text="?"),
#     KeyboardButton(text="?"),
# ],