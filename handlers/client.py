from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from db import bot_db


#@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'We are glad to welcome you to our car service', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Writing with bot only via private messages, write him:\nhttps://t.me/AutoServiceBot')


#@dp.message_handler(commands=['contacts'])
async def contacts_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Adress: https://www.google.com.ua/maps/place/50%C2%B004'06.1%22N+36%C2%B010'01.1%22E/@50.0683659,36.1664218,19z/data=!3m1!4b1!4m14!1m7!3m6!1s0x4127a477233095e7:0xec382a76d3b6360f!2z0JzQsNC70LDRjyDQlNCw0L3QuNC70L7QstC60LAsINCl0LDRgNGM0LrQvtCy0YHQutCw0Y8g0L7QsdC70LDRgdGC0YwsIDYyMzQy!3b1!8m2!3d50.072026!4d36.162836!3m5!1s0x0:0x2bda98cff183543f!7e2!8m2!3d50.0683654!4d36.1669695?hl=ru\nTel: 0501111111(Viber, Telegram)\nWorking mode: Mon-Sat from 09:00 to 18:00")


async def services_command(message: types.Message):
    await bot_db.sql_read(message)


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(contacts_command, commands=['contacts'])
    dp.register_message_handler(services_command, commands=['services'])
