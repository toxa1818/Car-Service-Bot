from aiogram.utils import executor
from create_bot import dp
from db import bot_db


async def on_startup(_):
    print('Bot is online')
    bot_db.sql_start()


from handlers import client, admin, other

client.register_handler_client(dp)
admin.register_handlers_admin(dp)
other.register_handler_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
