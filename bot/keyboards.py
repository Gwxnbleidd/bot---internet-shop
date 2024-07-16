from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

basket = []

number_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                               keyboard=[
                                   [KeyboardButton(text="Поделиться номером", request_contact=True)],
                               ])

promocode_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                               keyboard=[
                                   [KeyboardButton(text="У меня нет промокода")],
                               ])

main_menu = InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='Дополнительная информация', callback_data='info')],
                                 [InlineKeyboardButton(text='К покупкам', callback_data='purchases')],
                                 [InlineKeyboardButton(text='Корзина', callback_data='basket')],
                                 [InlineKeyboardButton(text='Реферальная программа', callback_data='referral_prog')]
                                 ])

back_button = InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='В главное меню', callback_data='back')],
                                 ])

purchases_menu = InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='Картриджи', callback_data='purchases_cartridges')],
                                 [InlineKeyboardButton(text='Жидкости', callback_data='purchases_liquids')],
                                 [InlineKeyboardButton(text='В главное меню', callback_data='back')]
                                 ])

def form_keyboard_purchasing_cartridges():
    #cartridges = get_list_of_cartridges()
    cartridges = ['Перый картридж', 'Второй картридж', 'Третий картридж']
    keyboard = [[InlineKeyboardButton(text=name, callback_data=f'purchases_cartridges_{id}')] 
                for id,name in enumerate(cartridges)]
    keyboard.append([InlineKeyboardButton(text='В меню покупок', callback_data='back_purchases')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


purchases_liquids_alcohol_strength_menu = InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='Крепкие', callback_data='purchases_liquids_strong')],
                                 [InlineKeyboardButton(text='Легкие', callback_data='purchases_liquids_lungs')],
                                 [InlineKeyboardButton(text='Все', callback_data='purchases_liquids_all')],
                                 [InlineKeyboardButton(text='В меню покупок', callback_data='back_purchases')]
                                 ])

purchases_liquids_alcohol_strength_strong_menu = InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='C холодком', callback_data='purchases_liquids_strong_cold')],
                                 [InlineKeyboardButton(text='Без холодка', callback_data='purchases_liquids_strong_not_cold')],
                                 [InlineKeyboardButton(text='В меню жидкостей', callback_data='back_purchases_liquids')]
                                 ])

purchases_liquids_alcohol_strength_lungs_menu = InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='C холодком', callback_data='purchases_liquids_lungs_cold')],
                                 [InlineKeyboardButton(text='Без холодка', callback_data='purchases_liquids_lungs_not_cold')],
                                 [InlineKeyboardButton(text='В меню жидкостей', callback_data='back_purchases_liquids')]
                                 ])

# Нужен не enumerate а просто доставать id
# будет просто список алкоголя

def form_strong_cold_keyboard():
    # alco = get_strong_cold_alco()
    alco = ['Водка мятная', 'Водка со льдом']
    keyboard = [[InlineKeyboardButton(text=name, callback_data=f'purchases_liquid_{id}')] 
                for id,name in enumerate(alco)]
    keyboard.append([InlineKeyboardButton(text='В меню жидкостей', callback_data='back_purchases_liquids')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def form_strong_not_cold_keyboard():
    # alco = get_strong_not_cold_alco()
    alco = ['Водка', 'Йегермейстер']
    keyboard = [[InlineKeyboardButton(text=name, callback_data=f'purchases_liquid_{id}')] 
                for id,name in enumerate(alco)]
    keyboard.append([InlineKeyboardButton(text='В меню жидкостей', callback_data='back_purchases_liquids')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def form_lungs_cold_keyboard():
    # alco = get_lungs_cold_alco()
    alco = ['Коктейль со льдом', 'Мохито с мятой']
    keyboard = [[InlineKeyboardButton(text=name, callback_data=f'purchases_liquid_{id}')] 
                for id,name in enumerate(alco)]
    keyboard.append([InlineKeyboardButton(text='В меню жидкостей', callback_data='back_purchases_liquids')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def form_lungs_not_cold_keyboard():
    # alco = get_strong_not_cold_alco()
    alco = ['Сидр', 'Пиво']
    keyboard = [[InlineKeyboardButton(text=name, callback_data=f'purchases_liquid_{id}')] 
                for id,name in enumerate(alco)]
    keyboard.append([InlineKeyboardButton(text='В меню жидкостей', callback_data='back_purchases_liquids')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def form_all_alco_keyboard():
    # alco = get_all_alco()
    alco = ['Сидр', 'Пиво','Коктейль со льдом', 'Мохито с мятой','Водка', 'Йегермейстер','Водка мятная', 'Водка со льдом']
    keyboard = [[InlineKeyboardButton(text=name, callback_data=f'purchases_liquid_{id}')] 
                for id,name in enumerate(alco)]
    keyboard.append([InlineKeyboardButton(text='В меню жидкостей', callback_data='back_purchases_liquids')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

basket_menu =  InlineKeyboardMarkup(inline_keyboard=[
                                 [InlineKeyboardButton(text='Удалить товар', callback_data='basket_delete')],
                                 [InlineKeyboardButton(text='Заказать', callback_data='basket_buy')],
                                 [InlineKeyboardButton(text='В главное меню', callback_data='back')]
                                 ])

def form_basket_delete_keyboard(basket_list = None):
    #if not basket_list:
        #basket_list = get_basket_from_db()
    basket_list = ['Пиво', 'Водка', 'Первый картридж']
    keyboard = [[InlineKeyboardButton(text=name, callback_data=f'delete_basket_{id}')] 
                for id,name in enumerate(basket_list)]
    keyboard.append([InlineKeyboardButton(text='Готово', callback_data='basket')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
