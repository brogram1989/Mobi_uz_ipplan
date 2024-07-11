from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from tgbot.keyboards.inline import MainMenu, MenuIP
user_router = Router()
from aiogram.fsm.context import FSMContext
import pandas as pd
from aiogram.types import InputFile
import logging
import os
@user_router.message(CommandStart())
@user_router.message(Command("menu"))
async def user_start(message: Message):
    await message.answer("Выберите меню", reply_markup=MainMenu)
@user_router.callback_query(F.data == "to_mainmenu")
async def user_start2(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text("Выберите нужный вам кнопки!",
                                  reply_markup=MainMenu)



@user_router.callback_query(F.data == "mw")
async def show_menu(query: CallbackQuery):
    await query.answer("Menuni tanglang")
    await query.message.edit_text("выбирайте нужный вам кнопки!",
                                  reply_markup=MenuIP)


# Reset command handler to reset the state
@user_router.message(Command('reset'))
async def cmd_reset(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("State has been reset.")

