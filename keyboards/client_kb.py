from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


b1 = KeyboardButton('/contacts')
b2 = KeyboardButton('/services')
b3 = KeyboardButton('request a consultation', request_contact=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.row(b1, b2).add(b3)
