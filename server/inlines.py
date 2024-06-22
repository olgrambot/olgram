from aiocache import cached
import hashlib
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.bot import Bot as AioBot

from olgram.models.models import Bot
import typing as ty


@cached(ttl=60)
async def get_phrases(bot: Bot) -> ty.List:
    objects = await bot.answers
    return [obj.text for obj in objects]


async def check_chat_member(chat_id: int, user_id: int, bot: AioBot) -> bool:
    member = await bot.get_chat_member(chat_id, user_id)
    return member.is_chat_member()


@cached(ttl=60)
async def check_permissions(inline_query: InlineQuery, bot: Bot):
    user_id = inline_query.from_user.id
    super_chat_id = await bot.super_chat_id()

    if super_chat_id == user_id:
        return True

    if super_chat_id < 0:  # Group chat
        is_member = await check_chat_member(super_chat_id, user_id, inline_query.bot)
        return is_member

    return False


async def inline_handler(inline_query: InlineQuery, bot: Bot):
    # Check permissions at first
    allow = await check_permissions(inline_query, bot)
    if not allow:
        return await inline_query.answer([])  # forbidden

    all_phrases = await get_phrases(bot)
    phrases = [phrase for phrase in all_phrases if inline_query.query.lower() in phrase.lower()]
    items = []
    for phrase in phrases:

        input_content = InputTextMessageContent(phrase)
        result_id: str = hashlib.md5(phrase.encode()).hexdigest()
        item = InlineQueryResultArticle(
            id=result_id,
            title=phrase,
            input_message_content=input_content,
        )
        items.append(item)

    await inline_query.answer(results=items)
