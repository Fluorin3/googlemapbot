import requests
import bs4
import app.classes as classes 
from aiogram import Bot, Dispatcher
import asyncio
from app.handlers import router
from multiprocessing import Process

with open('token.txt', 'r') as f:
    TOKEN = str(f.read())

bot = Bot(token=TOKEN)
dip = Dispatcher()

async def main():

    dip.include_router(router=router)

    await dip.start_polling(bot)


    
def run_main():
    asyncio.run(main())

if __name__ == '__main__':
    run_main()