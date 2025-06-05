import requests
import bs4
import app.classes as classes 
from aiogram import Bot, Dispatcher
import asyncio
from app.database import Database
from app.handlers import db
from main import bot, dip
import os


async def term():
    while True:
        term = input('Write command: ')
        if term == 'tz':
            msq = input("Input message: ")
            ids = db.get_users().fetchall()
            print(ids)
            for id in ids:
                id = int(dict(id._mapping)['id'])
                print(type(id))
                await bot.send_message(chat_id=id, text=msq)

        elif term == 'set token':
            with open('token.txt', 'w') as f:
                token = str(input("Input token: "))
                f.write(token)        
        elif term == 'exit':
            break
        else:
            pass

asyncio.run(term())