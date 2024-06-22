"""
Здесь работа с ботами на первом уровне вложенности: список ботов, добавление ботов
"""
from aiogram import types, Bot as AioBot
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import Unauthorized, TelegramAPIError
from tortoise.exceptions import IntegrityError
import re
from textwrap import dedent

from olgram.models.models import Bot, User
from olgram.settings import OlgramSettings, BotSettings
from olgram.commands.menu import send_bots_menu
from server.server import register_token
from locales.locale import _

from olgram.router import dp

import logging

logger = logging.getLogger(__name__)


token_pattern = r'[0-9]{8,10}:[a-zA-Z0-9_-]{35}'


@dp.message_handler(commands=["mybots"], state="*")
async def my_bots(message: types.Message, state: FSMContext):
    """
    Команда /mybots (список ботов)
    """
    return await send_bots_menu(message.chat.id, message.from_user.id)


@dp.message_handler(commands=["addbot"], state="*")
async def add_bot(message: types.Message, state: FSMContext):
    """
    Команда /addbot (добавить бота)
    """
    user = await User.get_or_none(telegram_id=message.from_user.id)
    max_bot_count = OlgramSettings.max_bots_per_user()
    if user and await user.is_promo():
        max_bot_count = OlgramSettings.max_bots_per_user_promo()
    bot_count = await Bot.filter(owner__telegram_id=message.from_user.id).count()
    if bot_count >= max_bot_count:
        await message.answer(_("У вас уже слишком много ботов. Удалите какой-нибудь свой бот из Olgram"
                               "(/mybots -> (Выбрать бота) -> Удалить бот)"))
        return

    await message.answer(dedent(_("""
    Чтобы подключить бот, вам нужно выполнить три действия:

    1. Перейдите в бот @BotFather, нажмите START и отправьте команду /newbot
    2. Введите название бота, а потом username бота.
    3. После создания бота перешлите ответное сообщение в этот бот или скопируйте и пришлите token бота.

    Важно: не подключайте боты, которые используются в других сервисах (Manybot, Chatfuel, Livegram и других).
    """)))
    await state.set_state("add_bot")


@dp.message_handler(state="add_bot", content_types="text", regexp="^[^/].+")  # Not command
async def bot_added(message: types.Message, state: FSMContext):
    """
    Пользователь добавляет бота и мы ждём от него токен
    """
    token = re.findall(token_pattern, message.text)

    async def on_invalid_token():
        await message.answer(dedent(_("""
        Это не токен бота.

        Токен выглядит вот так: 123456789:AAAA-abc123_AbcdEFghijKLMnopqrstu12
        """)))

    async def on_dummy_token():
        await message.answer(dedent(_("""
        Не удалось запустить этого бота: неверный токен
        """)))

    async def on_unknown_error():
        await message.answer(dedent(_("""
        Не удалось запустить этого бота: непредвиденная ошибка
        """)))

    async def on_duplication_bot():
        await message.answer(dedent(_("""
        Такой бот уже есть в базе данных
        """)))

    if not token:
        return await on_invalid_token()

    token = token[0]

    try:
        test_bot = AioBot(token)
        test_bot_info = await test_bot.get_me()
        await test_bot.session.close()
    except ValueError:
        return await on_invalid_token()
    except Unauthorized:
        return await on_dummy_token()
    except TelegramAPIError:
        return await on_unknown_error()

    if token == BotSettings.token():
        return await on_duplication_bot()

    user, created = await User.get_or_create(telegram_id=message.from_user.id)
    bot = Bot(token=Bot.encrypted_token(token), owner=user, name=test_bot_info.username,
              super_chat_id=message.from_user.id)
    try:
        await bot.save()
    except IntegrityError:
        return await on_duplication_bot()

    if not await register_token(bot):
        await bot.delete()
        return await on_unknown_error()

    await message.answer(_("Бот добавлен! Список ваших ботов: /mybots"))
    await state.reset_state()
