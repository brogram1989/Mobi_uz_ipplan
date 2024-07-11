from aiogram import Bot, Dispatcher
from tgbot.config import load_config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

config = load_config(".env")
def get_storage(config):
    """
    Return storage based on the provided configuration.

    Args:
        config (Config): The configuration object.

    Returns:
        Storage: The storage object based on the configuration.

    """
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


storage = get_storage(config)
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
dp = Dispatcher(storage=storage)

__all__ = ["bot", "dp", "config", "storage"]