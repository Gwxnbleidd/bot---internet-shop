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

user_router = Router()

class RegisterFrom(StatesGroup):
    name: str = State()
    number: str = State()
    promocode: str = State()

@user_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    if not get_user_from_db(message.from_user.id):
        await message.answer(f'Привет! Мы интернет - магазин Mango.\nВижу ты новый пользователь.\n'
                              'Давай зарегистрируемся!\n\nВведи свое имя ')
        await state.set_state(RegisterFrom.name)
    else:
        await message.answer(f'Привет! Мы интернет - магазин Mango.\n\nГлавное меню:', reply_markup=main_menu)

@user_router.message(RegisterFrom.name)
async def register_phone(message: Message, state: FSMContext):
    await state.update_data(name=message.text) 
    await message.answer(f"Приятно познакомиться, {message.text}!\n"
                         "Пожалуйста, поделитесь своим номером", reply_markup=number_button)
    await state.set_state(RegisterFrom.number)

@user_router.message(RegisterFrom.number)
async def register_promocode(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    await message.answer(f"Отлично!\nУкажите промокод друга, который вас пригласил", reply_markup=promocode_button)
    await state.set_state(RegisterFrom.promocode)

@user_router.message(RegisterFrom.promocode)
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

@user_router.callback_query(F.data == 'info')
async def print_info(callback: CallbackQuery):
    # text = get_text()
    text = 'Тут доп инфа, которую по идее меняет админ'
    await callback.message.edit_text(text,reply_markup=main_menu)

@user_router.callback_query(F.data == 'purchases')
async def print_purchases(callback: CallbackQuery):
    await callback.message.edit_text('Меню выбора: ',reply_markup=purchases_menu)

@user_router.callback_query(F.data == 'purchases_cartridges')
async def print_purchases(callback: CallbackQuery):
    cartridges = get_cartridges()
    info = 'Картриджи:\n'
    for id, name, price, quantity in cartridges:
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_keyboard_purchasing_cartridges(cartridges)
    await callback.message.edit_text(text=info,reply_markup=keyboard)


@user_router.callback_query(F.data == 'purchases_liquids')
async def print_purchases(callback: CallbackQuery):
    keyboard = purchases_liquids_alcohol_strength_menu
    await callback.message.edit_text('Выберите крепкость: ',reply_markup=keyboard)

# алкоголь крепкий---------
@user_router.callback_query(F.data == 'purchases_liquids_strong')
async def print_purchases(callback: CallbackQuery):
    keyboard = purchases_liquids_alcohol_strength_strong_menu
    await callback.message.edit_text('Выберите: ',reply_markup=keyboard)

@user_router.callback_query(F.data == 'purchases_liquids_strong_cold')
async def print_purchases(callback: CallbackQuery):
    alco = get_liquid(strength=True,cold=True)
    info = 'Алкоголь:\n'
    for _,name,_,_,price,quantity in alco:
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_strong_cold_keyboard(alco)
    await callback.message.edit_text(text=info,reply_markup=keyboard)

@user_router.callback_query(F.data == 'purchases_liquids_strong_not_cold')
async def print_purchases(callback: CallbackQuery):
    alco = get_liquid(strength=True,cold=False)
    info = 'Алкоголь:\n'
    for _,name,_,_,price,quantity in alco:
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_strong_cold_keyboard(alco)
    await callback.message.edit_text(text=info,reply_markup=keyboard)

# алкоголь легкий---------
@user_router.callback_query(F.data == 'purchases_liquids_lungs')
async def print_purchases(callback: CallbackQuery):
    keyboard = purchases_liquids_alcohol_strength_lungs_menu
    await callback.message.edit_text('Выберите: ',reply_markup=keyboard)

@user_router.callback_query(F.data == 'purchases_liquids_lungs_cold')
async def print_purchases(callback: CallbackQuery):
    alco = get_liquid(strength=False,cold=True)
    info = 'Алкоголь:\n'
    for _,name,_,_,price,quantity in alco:
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_strong_cold_keyboard(alco)
    await callback.message.edit_text(text=info,reply_markup=keyboard)

@user_router.callback_query(F.data == 'purchases_liquids_lungs_not_cold')
async def print_purchases(callback: CallbackQuery):
    alco = get_liquid(strength=True,cold=False)
    info = 'Алкоголь:\n'
    for _,name,_,_,price,quantity in alco:
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_strong_cold_keyboard(alco)
    await callback.message.edit_text(text=info,reply_markup=keyboard)

# алкоголь весь --------
@user_router.callback_query(F.data == 'purchases_liquids_all')
async def print_purchases(callback: CallbackQuery):
    alco = get_liquid()
    info = 'Алкоголь:\n'
    for _,name,_,_,price,quantity in alco:
        info += f'{name}\nЦена: {price}\nКоличество: {quantity}\n\n'
    keyboard = form_strong_cold_keyboard(alco)
    await callback.message.edit_text(text=info,reply_markup=keyboard)

#корзина----------------------
basket_list = ['Пиво', 'Водка', 'Первый картридж']
@user_router.callback_query(F.data == 'basket')
async def print_purchases(callback: CallbackQuery):
    text = '\n'.join(basket_list)
    await callback.message.edit_text(f'Корзина:\n{text}',reply_markup=basket_menu)

@user_router.callback_query(F.data == 'basket_delete')
async def print_purchases(callback: CallbackQuery):
    keyboard = form_basket_delete_keyboard()
    await callback.message.edit_text(f'Выберите какие товары удалить',reply_markup=keyboard)

#Реферальная программа------------
@user_router.callback_query(F.data == 'referral_prog')
async def print_purchases(callback: CallbackQuery):
    user = get_user_from_db(callback.from_user.id)
    await callback.message.edit_text(f'Ваш промокод: {user.promocode}\nКоличество друзей, которых вы привели: {user.number_of_guests}', reply_markup= main_menu)

# Кнопки назад
@user_router.callback_query(F.data == 'back_purchases_liquids')
async def print_purchases(callback: CallbackQuery):
    keyboard = purchases_liquids_alcohol_strength_menu
    await callback.message.edit_text('Выберите крепкость: ',reply_markup=keyboard)

@user_router.callback_query(F.data == 'back_purchases')
async def print_purchases(callback: CallbackQuery):
    await callback.message.edit_text('Меню выбора: ',reply_markup=purchases_menu)

@user_router.callback_query(F.data == 'back')
async def print_info(callback: CallbackQuery):
    await callback.message.edit_text('Главное меню: ',reply_markup=main_menu)



