from aiogram import Router, F
import aiogram as ag
import aiogram.filters
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from app.classes import Parser, Review_Parser
from app.database import Database
import asyncio

router = Router()
db = Database("d.db")
db.create_table()

class Form(StatesGroup):
    place = State()
    count = State()
    link = State()
    rev_count = State()

@router.message(aiogram.filters.CommandStart())
async def cmd_start(message: aiogram.types.Message):
    await message.answer('Здравствуйте! Добро пожаловать в Google map поисковик. \n Введите команду /set для задания места. \n Введите /rev для получения отзывов')
    id = int(message.chat.id)
    db.insert_user(id)
    

@router.message(aiogram.filters.Command('help'))
async def help_command(message: aiogram.types.Message):
    await message.answer('/')

@router.message(aiogram.filters.Command('set'))
async def filter_basic_command(message: aiogram.types.Message, state: FSMContext):
    await state.set_state(Form.place)
    await message.answer('Напишите место')
@router.message(Form.place)
async def get(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(place=message.text)
    await state.set_state(Form.count)
    await message.answer('Введите количество ожидаемых результатов')

@router.message(Form.count)
async def get2(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(count=message.text)
    await message.answer("Обработка запроса...")

    data = await state.get_data()
    await state.clear()
    p = Parser(data['place'], data['count'])
    p.parse()
    list = p.get_answer()
    for dict in list:
        string = 'Название: '+dict['name']+'\nАдресс: '+dict['Адресс']+'\nПлюс-код: '+dict['Plus-код']+'\nРейтинг: '+dict['R']+'\nСсылка на google map: '+dict['href']
        await message.answer(string)

@router.message(aiogram.filters.Command('rev'))
async def review1(message: aiogram.types.Message, state: FSMContext):
    await message.answer('Введите ссылку на google maps')
    await state.set_state(Form.link)

@router.message(Form.link)
async def review2(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer('Введите число ожидаемых отзывов(не более 10)')
    await state.set_state(Form.rev_count)

@router.message(Form.rev_count)
async def review3(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(rev_count=message.text)
    await message.answer("Обработка запроса...")
    data = await state.get_data()
    p = Review_Parser(data['link'], int(data['rev_count']))
    p.parse()
    list = p.get_answer()
    for dict in list:
        string = 'Никнейм: '+dict['nickname']+'\n Отзыв: \n'+str(dict['review']).replace('Нравится', '').replace('', '').replace('Поделиться', '').replace('', '').strip()+'\n Оценка: '+dict['rate']
        await message.answer(string)