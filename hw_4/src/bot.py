from aiogram import Bot, Dispatcher, types 
from aiogram.filters import Command 
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from config import TOKEN
from handlers import facts

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(facts.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
