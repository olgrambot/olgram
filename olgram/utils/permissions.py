import aiogram.types as types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
import typing as ty
from locales.locale import _


def public():
    """
    Хендлеры с этим декоратором будут обрабатываться даже если пользователь не является владельцем бота
    (например, команда /help)
    :return:
    """

    def decorator(func):
        setattr(func, "access_public", True)
        return func

    return decorator


class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_chat_ids: ty.Iterable[int]):
        self._access_chat_ids = access_chat_ids
        super(AccessMiddleware, self).__init__()

    @classmethod
    def _is_public_command(cls) -> bool:
        handler = current_handler.get()
        return handler and getattr(handler, "access_public", False)

    async def on_process_message(self, message: types.Message, data: dict):
        admin_ids = self._access_chat_ids
        if not admin_ids:
            return  # Администраторы бота вообще не указаны

        if self._is_public_command():  # Эта команда разрешена всем пользователям
            return

        if message.chat.id not in admin_ids:
            await message.answer(_("Владелец бота ограничил доступ к этому функционалу 😞"))
            raise CancelHandler()

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        admin_ids = self._access_chat_ids
        if not admin_ids:
            return  # Администраторы бота вообще не указаны

        if self._is_public_command():  # Эта команда разрешена всем пользователям
            return

        if call.message.chat.id not in admin_ids:
            await call.answer(_("Владелец бота ограничил доступ к этому функционалу😞"))
            raise CancelHandler()
