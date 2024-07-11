from aiogram import Router, F, Bot, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import CallbackQuery, BotCommand, File, Message, InputFile
from aiogram.utils.formatting import as_section, as_key_value, as_marked_list



menu_router = Router()


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
                         "\ntelegram: t.me/Gafurov_Dilshod"
                         "\nGitHub: https://github.com/brogram1989/"
                         "\n📱1: +998 88 989 87 23"
                         "\n📱2: +998 99 889 87 23")

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="start bot"),
        BotCommand(command="/menu", description="Show main menu"),
        BotCommand(command="/reset", description="reset some state"),
        BotCommand(command="/how_to_use", description="documentation"),
        BotCommand(command="/download_log", description="download log file"),
        BotCommand(command="/help", description="Show help"),
    ]
    await bot.set_my_commands(commands)

#_________________________________________________________________________#

