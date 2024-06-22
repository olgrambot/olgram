"""
Здесь простые команды на первом уровне вложенности: /start /help
"""

from aiogram import types
from aiogram.dispatcher import FSMContext
from textwrap import dedent
from olgram.settings import OlgramSettings
from olgram.utils.permissions import public
from locales.locale import _

from olgram.router import dp


@dp.message_handler(commands=["start"], state="*")
@public()
async def start(message: types.Message, state: FSMContext):
    """
    Команда /start
    """
    await state.reset_state()

    await message.answer(dedent(_("""
    Olgram Bot — это конструктор ботов обратной связи в Telegram. Подробнее \
<a href="https://olgram.readthedocs.io">читайте здесь</a>. Следите за обновлениями \
<a href="https://t.me/civsoc_it">здесь</a>.

    Используйте эти команды, чтобы управлять этим ботом:

    /addbot - добавить бот
    /mybots - управление ботами

    /help - помощь
    """)), parse_mode="html", disable_web_page_preview=True)


@dp.message_handler(commands=["help"], state="*")
@public()
async def help(message: types.Message, state: FSMContext):
    """
    Команда /help
    """
    await message.answer(dedent(_("""
    Читайте инструкции на нашем сайте https://olgram.readthedocs.io
    Техническая поддержка: @civsocit_feedback_bot
    Версия {0}
    """)).format(OlgramSettings.version()))


@dp.message_handler(commands=["chatid"], state="*")
@public()
async def chat_id(message: types.Message, state: FSMContext):
    """
    Команда /chatid
    """
    await message.answer(message.chat.id)
