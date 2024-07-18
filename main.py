from aiogram import Bot, Dispatcher
import asyncio

from bot.config import TOKEN

from bot.handlers.register_and_info_and_referal import register_router
from bot.handlers.cartridges import cartridges_router
from bot.handlers.liquids import liquids_router
from bot.handlers.basket import basket_router

dp = Dispatcher()

async def main():
    
    # create_tables()
    
    bot = Bot(TOKEN)
    dp.include_routers(register_router,cartridges_router,liquids_router,basket_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())