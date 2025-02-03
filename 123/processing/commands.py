import sqlite3
from kb import *
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

async def process_start_command(message):
    cursor.execute('SELECT * FROM users')
    if message.from_user.id not in cursor.fetchall():
        cursor.execute('INSERT INTO bin_data (id) VALUES (?)', (int(message.from_user.id),))
        conn.commit()
    await message.answer('Ваши данные были внесены в базу.', reply_markup=main_keyboard)