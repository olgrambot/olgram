"""Наши собственные миграции, которые нельзя описать на языке SQL и с которыми не справится TortoiseORM/Aerich"""

import aioredis
from tortoise import transactions, Tortoise
from olgram.settings import TORTOISE_ORM, ServerSettings
from olgram.models.models import MetaInfo, Bot
import logging


async def upgrade_1():
    """Шифруем токены"""
    meta_info = await MetaInfo.first()
    if meta_info.version != 0:
        logging.info("skip")
        return

    async with transactions.in_transaction():
        bots = await Bot.all()
        for bot in bots:
            bot.token = bot.encrypted_token(bot.token)
            await bot.save()
        meta_info.version = 1
        await meta_info.save()
    logging.info("done")


async def upgrade_2():
    """Отменяем малый TTL для старых сообщений"""
    meta_info = await MetaInfo.first()
    if meta_info.version != 1:
        logging.info("skip")
        return

    con = await aioredis.create_connection(ServerSettings.redis_path())
    client = aioredis.Redis(con)

    i, keys = await client.scan()
    for key in keys:
        if not key.startswith(b"thread"):
            await client.pexpire(key, ServerSettings.redis_timeout_ms())

    meta_info.version = 2
    await meta_info.save()
    logging.info("done")


async def upgrade_3():
    """start_text и second_text должны быть валидными HTML"""
    import html

    meta_info = await MetaInfo.first()
    if meta_info.version != 2:
        logging.info("skip")
        return

    async with transactions.in_transaction():
        bots = await Bot.all()
        for bot in bots:
            if bot.start_text:
                bot.start_text = html.escape(bot.start_text)
            if bot.second_text:
                bot.second_text = html.escape(bot.second_text)
            await bot.save(update_fields=["start_text", "second_text"])
        meta_info.version = 3
        await meta_info.save()
    logging.info("done")


# Не забудь добавить миграцию в этот лист!
_migrations = [upgrade_1, upgrade_2, upgrade_3]


async def migrate():
    logging.info("Run custom migrations...")
    await Tortoise.init(config=TORTOISE_ORM)

    for migration in _migrations:
        logging.info(f"Migration {migration.__name__}...")
        await migration()
