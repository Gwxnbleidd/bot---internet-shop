import re
from aiogram import Router,F
from aiogram.types import CallbackQuery

from bot.keyboards import basket_menu, form_basket_delete_keyboard
from database.orm import get_basket,delete_product_from_basket

basket_router = Router()

#корзина----------------------
@basket_router.callback_query(F.data == 'basket')
async def print_purchases(callback: CallbackQuery):
    basket_list = get_basket(callback.from_user.id)
    info='Корзина:\n'
    sum = 0
    for _,user_id_,name,price,quantity in basket_list:
        sum += price
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    info += f'Итого: {sum}'
    await callback.message.edit_text(text=info,reply_markup=basket_menu)

@basket_router.callback_query(F.data == 'basket_delete')
async def print_purchases(callback: CallbackQuery):
    keyboard = form_basket_delete_keyboard(callback.from_user.id)
    await callback.message.edit_text(f'Выберите какие товары удалить:',reply_markup=keyboard)

@basket_router.callback_query(lambda x: re.search('basket_delete_', x.data))
async def delete_from_basket(callback: CallbackQuery):
    id = int(callback.data.split('_')[-1])
    try:
        delete_product_from_basket(id)
        await callback.answer(f'Продукт удален из корзины')
    except Exception as e:
        await callback.answer(f'Вы не авторизованы, введите /start')