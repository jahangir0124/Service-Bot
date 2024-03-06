import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import sys
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import *
from state import *
TOKEN = "Token"
router = Router()

form_router = Router()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
@form_router.message(CommandStart())
@form_router.message(F.text =="В главное меню")
async def command_start_handler(message: Message, state: FSMContext) -> None:
    text = "добро пожаловать в наш бот!\nвыберите:"
    btns = createCatBtn()
    createUser(message.from_user)
    await message.answer(text, reply_markup=btns.as_markup(resize_keyboard=True))
    
    await state.set_state(ServiceState.catName)

@form_router.message(ServiceState.catName)
async def get_cat(message: Message, state: FSMContext):
    await state.update_data(catName=message.text)
    serBtn = (createServcieBtn(message.text))
    if serBtn:
        await message.answer("выберите: ", reply_markup=serBtn.as_markup(resize_keyboard=True))
        await state.set_state(ServiceState.serName)
    else:
        await message.answer("Hozircha bu bo'limda hech qanday xizmat\nmavjud emas!\nIltimos boshqa bo'limni tanlang1")

@form_router.message(ServiceState.serName)
async def get_Service(message: Message, state: FSMContext):
    await state.update_data(catName=message.text)
    numberBtn = ReplyKeyboardBuilder()
    numberBtn.row((types.KeyboardButton(text="Отправить номер телефона", request_contact=True)))
    await message.answer("Введите номер телефона", reply_markup=numberBtn.as_markup(resize_keyboard=True))
    await state.set_state(ServiceState.phoneNumber)
    
@form_router.message(ServiceState.phoneNumber)
async def get_number(message: Message, state: FSMContext):
    await state.update_data(phoneNumber=message.contact.phone_number)
    homeBtn = ReplyKeyboardBuilder()
    homeBtn.add(types.KeyboardButton(text="В главное меню"))
    await message.answer("Наши эксперты свяжутся с вами,\n🤝 Благодарим за выбор нас", reply_markup=homeBtn.as_markup(resize_keyboard=True))
    await state.clear()
async def main() -> None:
    
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)








if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
