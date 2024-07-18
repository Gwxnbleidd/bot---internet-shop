import re
from aiogram import Router,F
from aiogram.types import CallbackQuery

from bot.keyboards import (purchases_liquids_alcohol_strength_lungs_menu, purchases_liquids_alcohol_strength_menu,
                           purchases_liquids_alcohol_strength_strong_menu,form_all_alco_keyboard,form_lungs_cold_keyboard,
                           form_lungs_not_cold_keyboard,form_strong_cold_keyboard,form_strong_not_cold_keyboard)

from database.orm import get_liquid,add_product_in_basket

liquids_router = Router()

@liquids_router.callback_query(F.data == 'purchases_liquids')
async def print_purchases(callback: CallbackQuery):
    keyboard = purchases_liquids_alcohol_strength_menu
    await callback.message.edit_text('Выберите крепкость: ',reply_markup=keyboard)

# алкоголь крепкий---------
@liquids_router.callback_query(F.data == 'purchases_liquids_strong')
async def print_purchases(callback: CallbackQuery):
    keyboard = purchases_liquids_alcohol_strength_strong_menu
    await callback.message.edit_text('Выберите: ',reply_markup=keyboard)

@liquids_router.callback_query(F.data == 'purchases_liquids_strong_cold')
async def print_purchases(callback: CallbackQuery):
    alco = get_liquid(strength=True,cold=True)
    info = 'Алкоголь:\n'
    for _,_,name,price,quantity,_,_ in alco:
        if quantity == 0:
            continue
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_strong_cold_keyboard(alco)
    await callback.message.edit_text(text=info,reply_markup=keyboard)

@liquids_router.callback_query(F.data == 'purchases_liquids_strong_not_cold')
async def print_purchases(callback: CallbackQuery):
    alco = get_liquid(strength=True,cold=False)
    info = 'Алкоголь:\n'
    for _,_,name,price,quantity,_,_ in alco:
        if quantity == 0:
            continue
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_strong_not_cold_keyboard(alco)
    await callback.message.edit_text(text=info,reply_markup=keyboard)

# алкоголь легкий---------
@liquids_router.callback_query(F.data == 'purchases_liquids_lungs')
async def print_purchases(callback: CallbackQuery):
    keyboard = purchases_liquids_alcohol_strength_lungs_menu
    await callback.message.edit_text('Выберите: ',reply_markup=keyboard)

@liquids_router.callback_query(F.data == 'purchases_liquids_lungs_cold')
async def print_purchases(callback: CallbackQuery):
    alco = get_liquid(strength=False,cold=True)
    info = 'Алкоголь:\n'
    for _,_,name,price,quantity,_,_ in alco:
        if quantity == 0:
            continue
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_lungs_cold_keyboard(alco)
    await callback.message.edit_text(text=info,reply_markup=keyboard)

@liquids_router.callback_query(F.data == 'purchases_liquids_lungs_not_cold')
async def print_purchases(callback: CallbackQuery):
    alco = get_liquid(strength=False,cold=False)
    info = 'Алкоголь:\n'
    for _,_,name,price,quantity,_,_ in alco:
        if quantity == 0:
            continue
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_lungs_not_cold_keyboard(alco)
    await callback.message.edit_text(text=info,reply_markup=keyboard)

# алкоголь весь --------
@liquids_router.callback_query(F.data == 'purchases_liquids_all')
async def print_purchases(callback: CallbackQuery):
    alco = get_liquid()
    info = 'Алкоголь:\n'
    for _,_,name,price,quantity,_,_ in alco:
        if quantity == 0:
            continue
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_all_alco_keyboard(alco)
    await callback.message.edit_text(text=info,reply_markup=keyboard)

@liquids_router.callback_query(lambda x: re.search('purchases_liquid_', x.data))
async def add_in_basket(callback: CallbackQuery):
    id = int(callback.data.split('_')[-1])
    try:
        id,name,price,quantity = get_liquid(id)
        add_product_in_basket(user_id=callback.from_user.id,product_id=id,product_name=name,
                              product_price=price,product_quantity=quantity)
        await callback.answer(f'Продукт {name} добавлен в корзину')
    except Exception as e:
        await callback.answer(f'Вы не авторизованы, введите /start')