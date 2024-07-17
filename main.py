from aiogram import Bot, Dispatcher
import asyncio

from bot.config import TOKEN
from bot.handlers import user_router
from database.orm import create_tables

dp = Dispatcher()

async def main():
    
    # create_tables()
    
    bot = Bot(TOKEN)
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())