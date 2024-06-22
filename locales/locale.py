import gettext
from olgram.settings import BotSettings
from os.path import dirname

locales_dir = dirname(__file__)


def dummy_translator(x: str) -> str:
    return x


lang = BotSettings.language()
if lang == "ru":
    _ = dummy_translator
else:
    t = gettext.translation("olgram", localedir=locales_dir, languages=[lang])
    _ = t.gettext


translators = {
    "ru": dummy_translator,
    "uk": gettext.translation("olgram", localedir=locales_dir, languages=["uk"]).gettext,
    "zh": gettext.translation("olgram", localedir=locales_dir, languages=["zh"]).gettext,
    "en": gettext.translation("olgram", localedir=locales_dir, languages=["en"]).gettext,
}
