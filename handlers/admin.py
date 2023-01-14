from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from db import bot_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


ID = None


class FSMAdmin(StatesGroup):
    name = State()
    price = State()
    duration = State()


async def make_change_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'You have access', reply_markup=admin_kb.kb_admin)
    await message.delete()


async def commands_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.name.set()
        await message.reply('Enter name')


async def cancel_set(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Canceled')


async def enter_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Enter price')


async def set_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text
        await FSMAdmin.next()
        await message.reply('Enter duration')


async def enter_duration(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['duration'] = message.text
        await bot_db.sql_add_command(state)
        await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await bot_db.sql_delete(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} is deleted", show_alert=True)


@dp.message_handler(commands='delete')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await bot_db.sql_read2()
        for r in read:
            await bot.send_message(message.from_user.id, f"{r[0]}\nPrice: {r[1]}\nDuration: {r[2]}")
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Delete service', callback_data=f'del {r[0]}')))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['add_service'], state=None)
    dp.register_message_handler(cancel_set, state="*", commands='cancel')
    dp.register_message_handler(enter_name, state=FSMAdmin.name)
    dp.register_message_handler(set_price, state=FSMAdmin.price)
    dp.register_message_handler(enter_duration, state=FSMAdmin.duration)
    dp.register_message_handler(make_change_command, commands='moderator', is_chat_admin=True)
