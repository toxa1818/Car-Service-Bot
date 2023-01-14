from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


load_b = KeyboardButton('/add_service')
delete_b = KeyboardButton('/delete')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(load_b).add(delete_b)
