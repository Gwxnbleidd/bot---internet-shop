import re

from aiogram import Router,F
from aiogram.types import CallbackQuery

from database.orm import get_cartridges
from bot.keyboards import form_keyboard_purchasing_cartridges
from database.orm import add_product_in_basket

cartridges_router = Router()

@cartridges_router.callback_query(F.data == 'purchases_cartridges')
async def print_purchases(callback: CallbackQuery):
    cartridges = get_cartridges()
    info = 'Картриджи:\n'
    for id, name, price, quantity in cartridges:
        if quantity == 0:
            continue
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_keyboard_purchasing_cartridges(cartridges)
    await callback.message.edit_text(text=info,reply_markup=keyboard)

@cartridges_router.callback_query(lambda x: re.search('purchases_cartridges_', x.data))
async def add_in_basket(callback: CallbackQuery):
    id = int(callback.data.split('_')[-1])
    try:
        id,name,price,quantity = get_cartridges(id)
        add_product_in_basket(callback.from_user.id,name,price,quantity)
        await callback.answer(f'Продукт {name} добавлен в корзину')
    except Exception as e:
        await callback.answer(f'Вы не авторизованы, введите /start')
