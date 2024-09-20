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
            await message.answer("Лог файл не нашли!")

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
        await message.answer("🚫 У Вас нет прав, Вы не ползователь!", reply_markup=ReplyKeyboardRemove())

# Handler to capture the broadcast message and send it to all users
@menu_router.message(F.text, FindId.send_msg)
async def broadcast_message(message: types.Message, state:FSMContext):
    if is_user(message.from_user.id):
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
        await message.answer("🚫 У Вас нет прав, Вы не ползователь!")

#__________________________________________________________#


@menu_router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("This is the help desk. Choose an option:"
                         "\n/menu - показать главного меню"
                         "\n/reset - при неожиданного ситуатции сбросить все задачи бота"
                         "\n/download_log - загрузить лог файлы"
                         "\n/check_ip - сверить плановый ip адресов, с системой управлении"
                         "\n/send_message - отправить сообщения всем пользователям"
                         "\n/help - помощь"
                         "\n\n⌨️💻Этот бот написал Дилшод Гафуров"
                         "\nконтакты:"
                         "\ntelegram: t.me/Gafurov989"
                         "\nGitHub: https://github.com/brogram1989/"
                         "\n📱1: +998 88 989 87 23"
                         )

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/menu", description="показать главного меню"),
        BotCommand(command="/reset", description="при неожиданного ситуатции сбросить все задачи бота"),
        BotCommand(command="/download_log", description="загрузить лог файлы"),
        BotCommand(command="/check_ip", description="сверить плановый ip адресов, с системой управлении"),
        BotCommand(command="/send_message", description="отправить сообщения всем пользователям"),
        BotCommand(command="/help", description="помощь"),
    ]
    await bot.set_my_commands(commands)

#__________________________________________________________________________#

