"""
Здесь промокоды
"""


from aiogram import types
from aiogram.dispatcher import FSMContext
from olgram.models import models
from uuid import UUID

from olgram.router import dp
from olgram.settings import OlgramSettings
from locales.locale import _


@dp.message_handler(commands=["newpromo"], state="*")
async def new_promo(message: types.Message, state: FSMContext):
    """
    Команда /newpromo
    """

    if message.chat.id != OlgramSettings.supervisor_id():
        await message.answer(_("Недостаточно прав"))
        return

    promo = await models.Promo()
    await message.answer(_("Новый промокод\n```{0}```").format(promo.code), parse_mode="Markdown")

    await promo.save()


@dp.message_handler(commands=["delpromo"], state="*")
async def del_promo(message: types.Message, state: FSMContext):
    """
    Команда /delpromo
    """

    if message.chat.id != OlgramSettings.supervisor_id():
        await message.answer(_("Недостаточно прав"))
        return

    try:
        uuid = UUID(message.get_args().strip())
        promo = await models.Promo.get_or_none(code=uuid)
    except ValueError:
        return await message.answer(_("Неправильный токен"))

    if not promo:
        return await message.answer(_("Такого кода не существует"))

    user = await models.User.filter(promo=promo)
    bots = await user.bots()
    for bot in bots:
        bot.enable_olgram_text = True
        await bot.save(update_fields=["enable_olgram_text"])

    await promo.delete()

    await message.answer(_("Промокод отозван"))


@dp.message_handler(commands=["setpromo"], state="*")
async def setpromo(message: types.Message, state: FSMContext):
    """
    Команда /setpromo
    """

    arg = message.get_args()
    if not arg:
        return await message.answer(_("Укажите аргумент: промокод. Например: <pre>/setpromo my-promo-code</pre>"),
                                    parse_mode="HTML")

    arg = arg.strip()

    try:
        UUID(arg)
    except ValueError:
        return await message.answer(_("Промокод не найден"))

    promo = await models.Promo.get_or_none(code=arg)
    if not promo:
        return await message.answer(_("Промокод не найден"))

    if promo.owner:
        return await message.answer(_("Промокод уже использован"))

    user, created = await models.User.get_or_create(telegram_id=message.from_user.id)
    promo.owner = user
    await promo.save(update_fields=["owner_id"])

    await message.answer(_("Промокод активирован! Спасибо 🙌"))
