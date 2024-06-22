from aiogram import Bot as AioBot
from aiogram.types import BotCommand
from olgram.models.models import Bot
from aiohttp import web
from asyncio import get_event_loop
import ssl
from olgram.settings import ServerSettings
from locales.locale import _
from .custom import CustomRequestHandler

import logging


logger = logging.getLogger(__name__)


def path_for_bot(bot: Bot) -> str:
    return "/" + str(bot.code)


def url_for_bot(bot: Bot) -> str:
    return f"https://{ServerSettings.hook_host()}:{ServerSettings.hook_port()}" + path_for_bot(bot)


async def register_token(bot: Bot) -> bool:
    """
    Зарегистрировать токен
    :param bot: Бот
    :return: получилось ли
    """
    await unregister_token(bot.decrypted_token())

    a_bot = AioBot(bot.decrypted_token())
    certificate = None
    if ServerSettings.use_custom_cert():
        certificate = open(ServerSettings.public_path(), 'rb')

    res = await a_bot.set_webhook(url_for_bot(bot), certificate=certificate, drop_pending_updates=True,
                                  max_connections=10)
    await a_bot.set_my_commands([
        BotCommand("/start", _("(Пере)запустить бота")),
        BotCommand("/security_policy", _("Политика конфиденциальности"))
    ])

    await a_bot.session.close()
    del a_bot
    return res


async def unregister_token(token: str):
    """
    Удалить токен
    :param token: токен
    :return:
    """
    bot = AioBot(token)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    del bot


def main():
    loop = get_event_loop()

    app = web.Application()
    app.router.add_route('*', r"/{name}", CustomRequestHandler, name='webhook_handler')

    context = None
    if ServerSettings.use_custom_cert():
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(ServerSettings.public_path(), ServerSettings.priv_path())

    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    logger.info("Server initialization done")
    site = web.TCPSite(runner, port=ServerSettings.app_port(), ssl_context=context)
    return site
