"""
Здесь некоторые команды администратора
"""

from aiogram import types
from aiogram.dispatcher import FSMContext
from olgram.models import models

from olgram.router import dp
from olgram.settings import OlgramSettings
from locales.locale import _


@dp.message_handler(commands=["notifyowner"], state="*")
async def notify(message: types.Message, state: FSMContext):
    """
    Команда /notify-owner
    """

    if message.chat.id != OlgramSettings.supervisor_id():
        await message.answer(_("Недостаточно прав"))
        return

    bot_name = message.get_args()

    if not bot_name:
        await message.answer(_("Нужно указать имя бота"))
        return

    bot = await models.Bot.filter(name=bot_name.replace("@", "")).first()

    if not bot:
        await message.answer(_("Такого бота нет в системе"))
        return

    await state.set_state("wait_owner_notify_message")
    await state.update_data({"notify_to_bot": bot.id})

    markup = types.ReplyKeyboardMarkup([[types.KeyboardButton(text=_("Пропустить"))]],
                                       resize_keyboard=True)

    await message.answer(_("Введите текст, который будет отправлен владельцу бота {0}. "
                           "Напишите 'Пропустить' чтобы отменить").format(bot_name), reply_markup=markup)


@dp.message_handler(state="wait_owner_notify_message")
async def on_notify_text(message: types.Message, state: FSMContext):
    if not message.text:
        await state.reset_state(with_data=True)
        await message.answer(_("Поддерживается только текст"), reply_markup=types.ReplyKeyboardRemove())
        return

    if message.text == _("Пропустить"):
        await state.reset_state(with_data=True)
        await message.answer(_("Отменено"), reply_markup=types.ReplyKeyboardRemove())
        return

    await state.update_data({"notify_text": message.text})
    await state.set_state("wait_owner_notify_message_confirm")

    markup = types.ReplyKeyboardMarkup([[types.KeyboardButton(text=_("Отправить")),
                                         types.KeyboardButton(text=_("Отменить"))]], resize_keyboard=True)

    await message.answer("Точно отправить?", reply_markup=markup)


@dp.message_handler(state="wait_owner_notify_message_confirm")
async def on_notify_message_confirm(message: types.Message, state: FSMContext):
    if not message.text or (message.text != _("Отправить")):
        await state.reset_state(with_data=True)
        await message.answer(_("Отменено"), reply_markup=types.ReplyKeyboardRemove())
        return

    data = await state.get_data()
    bot = await models.Bot.get(pk=data["notify_to_bot"])
    text = data["notify_text"]
    chat_id = (await bot.owner).telegram_id

    await state.reset_state(with_data=True)
    await message.bot.send_message(chat_id, text=text)
    await message.answer(_("Отправлено"), reply_markup=types.ReplyKeyboardRemove())
