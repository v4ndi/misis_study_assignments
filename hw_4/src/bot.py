from aiogram import Bot, Dispatcher, types 
from aiogram.filters import Command 
from aiogram.fsm.storage.redis import RedisStorage, Redis
import asyncio
from config import TOKEN
from handlers import facts

async def main():
    bot = Bot(token=TOKEN)
    redis = Redis(host='localhost')

    dp = Dispatcher(storage=RedisStorage(redis=redis))

    dp.include_router(facts.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
