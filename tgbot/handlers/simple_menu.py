import csv
import io
import re
from collections import defaultdict
from datetime import datetime
from aiogram import Router, F, Bot, types
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import Command
from aiogram.types import CallbackQuery, BotCommand, File, Message, InputFile, ReplyKeyboardRemove
from aiogram.utils.formatting import as_section, as_key_value, as_marked_list
from .admin import is_admin, is_user
from tgbot.config import ADMINS, USERS
from aiogram.fsm.context import FSMContext
from tgbot.states.personalData import FindId


from loader import bot
import os
import pandas as pd
from io import BytesIO

menu_router = Router()
#_____________________________________________________________#
#log fileni download qilish
# Bot menu
@menu_router.message(Command("download_log"))
async def send_log_file(message: types.Message):
    try:
        #fayl yuborishdan oldin action qilish, yozyotganga o'xshab
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.UPLOAD_DOCUMENT,
        )
        log_file_path = os.path.join("logs", "excel_file.log")  # Path to your log file
        file = io.StringIO()
        csv_writer = csv.writer(file)
        if os.path.exists(log_file_path):

            # Read the log file into a Pandas DataFrame
            df = pd.read_csv(log_file_path, sep='\t')
            # Convert the DataFrame to a txt file
            for row in df.values:
                csv_writer.writerow(row)

            await message.reply_document(
                document=types.BufferedInputFile(
                    file=file.getvalue().encode("utf-8"),
                    filename=f'logfile_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
                )
            )
        else:
            await message.answer("Log file not found.")

    except Exception as e:
        await message.answer(f"Error occurred: {str(e)}")
#_______________________________________________________________#
#barcha userlarga xabar yuborish qismi

# Command to send broadcast message

@menu_router.message(Command("send_message"))
async def start_broadcast(message: types.Message, state: FSMContext):
    if is_admin(message.from_user.id):  # Assuming you have an is_admin check
        await message.answer("Напишите текст который Вы хотите отправить пользовотелям:")
        await state.set_state(FindId.send_msg)
    else:
        await message.answer("🚫 You are not authorized to use this command.", reply_markup=ReplyKeyboardRemove())

# Handler to capture the broadcast message and send it to all users
@menu_router.message(F.text, FindId.send_msg)
async def broadcast_message(message: types.Message, state:FSMContext):
    if is_admin(message.from_user.id):
        broadcast_text = message.text
        failed_users = []
        success_count = 0

        for user_id in USERS:
            try:
                await bot.send_message(chat_id=user_id, text=broadcast_text)
                success_count += 1
            except Exception as e:
                failed_users.append(user_id)
                print(f"Ошибка возникла при отправке на ползователь номером {user_id}: {e}")
            await state.clear()
        await message.answer(f"Сообшения отправлено {success_count} ползователям. Не отправлено {len(failed_users)} ползователям.")
    else:
        await message.answer("🚫 You are not authorized to broadcast messages.")

#__________________________________________________________#


@menu_router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("This is the help desk. Choose an option:"
                         "\n/menu - Show menu"
                         "\n/reset - for reseting some state"
                         "\n/download_log - download log files"
                         "\n/send_message - send message to users"
                         "\n/help - Show help"
                         "\n\n⌨️💻This bot is written by Dilshod Gafurov "
                         "\ncontacts:"
                         "\ntelegram: t.me/Gafurov989"
                         "\nGitHub: https://github.com/brogram1989/"
                         "\n📱1: +998 88 989 87 23"
                         )

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/menu", description="Show main menu"),
        BotCommand(command="/reset", description="reset some state"),
        BotCommand(command="/download_log", description="download log file"),
        BotCommand(command="/send_message", description="send message to users"),
        BotCommand(command="/help", description="Show help"),
    ]
    await bot.set_my_commands(commands)

#_________________________________________________________________________#

