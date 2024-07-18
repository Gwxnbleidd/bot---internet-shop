import secrets
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.keyboards import (form_lungs_cold_keyboard, form_lungs_not_cold_keyboard, number_button, promocode_button, main_menu,
                           purchases_menu, form_keyboard_purchasing_cartridges, purchases_liquids_alcohol_strength_menu,
                           purchases_liquids_alcohol_strength_strong_menu,form_strong_cold_keyboard, 
                           form_strong_not_cold_keyboard, purchases_liquids_alcohol_strength_lungs_menu, form_all_alco_keyboard,
                           basket_menu, form_basket_delete_keyboard)

from database.orm import add_user_in_db, get_user_from_db, get_cartridges, get_liquid

register_router = Router()

class RegisterFrom(StatesGroup):
    name: str = State()
    number: str = State()
    promocode: str = State()

@register_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if not get_user_from_db(message.from_user.id):
        await message.answer(f'Привет! Мы интернет - магазин Mango.\nВижу ты новый пользователь.\n'
                              'Давай зарегистрируемся!\n\nВведи свое имя ')
        await state.set_state(RegisterFrom.name)
    else:
        await message.answer(f'Привет! Мы интернет - магазин Mango.\n\nГлавное меню:', reply_markup=main_menu)

@register_router.message(RegisterFrom.name)
async def register_phone(message: Message, state: FSMContext):
    await state.update_data(name=message.text) 
    await message.answer(f"Приятно познакомиться, {message.text}!\n"
                         "Пожалуйста, поделитесь своим номером", reply_markup=number_button)
    await state.set_state(RegisterFrom.number)

@register_router.message(RegisterFrom.number)
async def register_promocode(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    await message.answer(f"Отлично!\nУкажите промокод друга, который вас пригласил", reply_markup=promocode_button)
    await state.set_state(RegisterFrom.promocode)

@register_router.message(RegisterFrom.promocode)
async def register_promocode(message: Message, state: FSMContext):
    promocode = message.text
    if promocode != 'У меня нет промокода':    
        await state.update_data(promocode=promocode)
    else:
        await state.update_data(promocode='')
    user = await state.get_data()
    token = secrets.token_hex(10)
    try:
        add_user_in_db(id=message.from_user.id,name=user['name'],number=user['number'],promocode=token)
        # Добавить пригласившему +1 
        await message.answer("Регистрация завершена!\nГлавное меню: ",reply_markup=main_menu)
        await state.clear()
    except Exception as e:
        await message.answer(e + '\nПожалуйста, поделитесь своим номером.')
        await state.set_state(RegisterFrom.number)

@register_router.callback_query(F.data == 'info')
async def print_info(callback: CallbackQuery):
    # text = get_text()
    text = 'Тут доп инфа, которую по идее меняет админ'
    await callback.message.edit_text(text,reply_markup=main_menu)

@register_router.callback_query(F.data == 'purchases')
async def print_purchases(callback: CallbackQuery):
    await callback.message.edit_text('Меню выбора: ',reply_markup=purchases_menu)

#Реферальная программа------------
@register_router.callback_query(F.data == 'referral_prog')
async def print_purchases(callback: CallbackQuery):
    user = get_user_from_db(callback.from_user.id)
    await callback.message.edit_text(f'Ваш промокод: {user.promocode}\nКоличество друзей, которых вы привели: {user.number_of_guests}', reply_markup= main_menu)

# Кнопки назад
@register_router.callback_query(F.data == 'back_purchases_liquids')
async def print_purchases(callback: CallbackQuery):
    keyboard = purchases_liquids_alcohol_strength_menu
    await callback.message.edit_text('Выберите крепкость: ',reply_markup=keyboard)

@register_router.callback_query(F.data == 'back_purchases')
async def print_purchases(callback: CallbackQuery):
    await callback.message.edit_text('Меню выбора: ',reply_markup=purchases_menu)

@register_router.callback_query(F.data == 'back')
async def print_info(callback: CallbackQuery):
    await callback.message.edit_text('Главное меню: ',reply_markup=main_menu)



