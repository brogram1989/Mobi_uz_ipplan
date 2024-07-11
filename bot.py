import asyncio
import logging
from pathlib import Path
import pandas as pd
from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, InputFile
from aiogram.filters.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from tgbot.config import load_config, Config
from tgbot.handlers import routers_list
from tgbot.handlers.simple_menu import set_commands
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.services import broadcaster
from loader import bot, dp, config
from logging_config import setup_logging  # Import the setup_logging function

class FindId(StatesGroup):
    send_ip_file = State()
    send_neid_file = State()
async def on_startup(bot: Bot, admin_ids: list[int]):
    await set_commands(bot)
    await broadcaster.broadcast(bot, admin_ids, "Bot ishga tushdi!")
    export_logs_to_csv()

def register_global_middlewares(dp: Dispatcher, config: Config, session_pool=None):
    middleware_types = [
        ConfigMiddleware(config),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)

def export_logs_to_csv():
    log_files = [
        Path("logs") / "excel_file.log",
    ]
    log_data = []

    for log_file in log_files:
        with open(log_file, "r") as f:
            for line in f:
                try:
                    if '|' in line:
                        timestamp, level, message = line.strip().split(" | ")
                        log_data.append({"timestamp": timestamp, "level": level, "message": message})
                    else:
                        log_data.append(line)
                except (ValueError, AttributeError) as e:
                    if isinstance(e, ValueError):
                        log_data.append(f"Can't read log in this time. ValueError: {e}")
                    elif isinstance(e, AttributeError):
                        log_data.append(f"Can't read log in this time. AttributeError: {e}")
                    else:
                        log_data.append(f"Can't read log in this time. Exception: {e}")
                except Exception as e:
                    log_data.append(f"Can't read log in this time. Exception: {e}")

    df = pd.DataFrame(log_data)
    df.to_csv("user_actions.csv", index=False)

    logger = logging.getLogger(__name__)
    logger.info("Exported user actions to user_actions.csv")

async def main():
    setup_logging()  # Set up logging

    dp.include_routers(*routers_list)
    register_global_middlewares(dp, config)

    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("bot ishni tugatdi!")
