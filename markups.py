from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def make_keyboard(arr):
    kl = ReplyKeyboardMarkup(resize_keyboard=True)

    for i in range(1, len(arr), 2):
        btn1 = KeyboardButton(arr[i-1])
        btn2 = KeyboardButton(arr[i])

        kl.add(btn1, btn2)

    if (len(arr) % 2 != 0):
        kl.add(KeyboardButton(arr[-1]))

    return kl
