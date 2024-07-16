import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.keyboards import (form_lungs_cold_keyboard, form_lungs_not_cold_keyboard, number_button, promocode_button, main_menu, back_button, 
                           purchases_menu, form_keyboard_purchasing_cartridges, purchases_liquids_alcohol_strength_menu,
                           purchases_liquids_alcohol_strength_strong_menu,form_strong_cold_keyboard, 
                           form_strong_not_cold_keyboard, purchases_liquids_alcohol_strength_lungs_menu, form_all_alco_keyboard,
                           basket_menu, form_basket_delete_keyboard)

user_router = Router()

class RegisterFrom(StatesGroup):
    name: str = State()
    number: str = State()
    promocode: str = State()

@user_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    #if not get_user_from_db(message.from_user.id):
    await message.answer(f'Привет! Мы интернет - магазин Mango.\nВижу ты новый пользователь.\n'
                              'Давай зарегистрируемся!\n\n Введи свое имя ')
    await state.set_state(RegisterFrom.name)
    #else:
        #await message.answer(f'Привет! Мы интернет - магазин Mango.\n Меню выбора')

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
    token = [random.randint(0,999) for _ in range(10)]
    #add_in_bd()
    await message.answer("Регистрация завершена!\nГлавное меню: ",reply_markup=main_menu)
    await state.clear()

@user_router.callback_query(F.data == 'info')
async def print_info(callback: CallbackQuery):
    await callback.message.edit_text('Тут доп инфа, которую по идее меняет админ',reply_markup=back_button)

@user_router.callback_query(F.data == 'purchases')
async def print_purchases(callback: CallbackQuery):
    await callback.message.edit_text('Меню выбора: ',reply_markup=purchases_menu)

@user_router.callback_query(F.data == 'purchases_cartridges')
async def print_purchases(callback: CallbackQuery):
    keyboard = form_keyboard_purchasing_cartridges()
    await callback.message.edit_text('Картриджи: ',reply_markup=keyboard)


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
    keyboard = form_strong_cold_keyboard()
    await callback.message.edit_text('Нажатие добавит в корзину: ',reply_markup=keyboard)

@user_router.callback_query(F.data == 'purchases_liquids_strong_not_cold')
async def print_purchases(callback: CallbackQuery):
    keyboard = form_strong_not_cold_keyboard()
    await callback.message.edit_text('Нажатие добавит в корзину: ',reply_markup=keyboard)

# алкоголь легкий---------
@user_router.callback_query(F.data == 'purchases_liquids_lungs')
async def print_purchases(callback: CallbackQuery):
    keyboard = purchases_liquids_alcohol_strength_lungs_menu
    await callback.message.edit_text('Выберите: ',reply_markup=keyboard)

@user_router.callback_query(F.data == 'purchases_liquids_lungs_cold')
async def print_purchases(callback: CallbackQuery):
    keyboard = form_lungs_cold_keyboard()
    await callback.message.edit_text('Нажатие добавит в корзину: ',reply_markup=keyboard)

@user_router.callback_query(F.data == 'purchases_liquids_lungs_not_cold')
async def print_purchases(callback: CallbackQuery):
    keyboard = form_lungs_not_cold_keyboard()
    await callback.message.edit_text('Нажатие добавит в корзину: ',reply_markup=keyboard)

# алкоголь весь --------
@user_router.callback_query(F.data == 'purchases_liquids_all')
async def print_purchases(callback: CallbackQuery):
    keyboard = form_all_alco_keyboard()
    await callback.message.edit_text('Нажатие добавит в корзину: ',reply_markup=keyboard)

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



