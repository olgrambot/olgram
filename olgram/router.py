from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .settings import BotSettings


bot = Bot(BotSettings.token())
dp = Dispatcher(bot, storage=MemoryStorage())
