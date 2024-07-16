from aiogram import Bot, Dispatcher
import asyncio

from bot.config import TOKEN
from bot.handlers import user_router

dp = Dispatcher()

async def main():
    bot = Bot(TOKEN)
    dp.include_router(user_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())