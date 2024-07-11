import csv
import io
from datetime import datetime
from aiogram import Router, F, Bot, types
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import Command
from aiogram.types import CallbackQuery, BotCommand, File, Message, InputFile
from aiogram.utils.formatting import as_section, as_key_value, as_marked_list

from loader import bot
import os
import pandas as pd
from io import BytesIO

menu_router = Router()

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
                    filename=f'logfile{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'
                )
            )

        else:
            await message.answer("Log file not found.")

    except Exception as e:
        await message.answer(f"Error occurred: {str(e)}")




@menu_router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("This is the help desk. Choose an option:"
                         "\n/start - start bot"
                         "\n/menu - Show menu"
                         "\n/reset - for reseting some state"
                         "\n/download_log - download log files"
                         "\n/help - Show help"
                         "\n\n⌨️💻This bot is written by Dilshod Gafurov "
                         "\ncontacts:"
                         "\ntelegram: t.me/Gafurov989"
                         "\nGitHub: https://github.com/brogram1989/"
                         "\n📱1: +998 88 989 87 23"
                         )

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="start bot"),
        BotCommand(command="/menu", description="Show main menu"),
        BotCommand(command="/reset", description="reset some state"),
        BotCommand(command="/download_log", description="download log file"),
        BotCommand(command="/help", description="Show help"),
    ]
    await bot.set_my_commands(commands)

#_________________________________________________________________________#

