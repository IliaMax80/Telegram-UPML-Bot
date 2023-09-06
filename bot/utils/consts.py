from typing import Final

from bot.utils.enums import SlashCommands


# Переводы всякого
CAFE_MENU_ENG_TO_RU: Final[dict[str, str]] = {
    "breakfast": "завтрак",
    "lunch": "второй завтрак",
    "dinner": "обед",
    "snack": "полдник",
    "supper": "ужин",
}
NOTIFIES_ENG_TO_RU: Final[dict[str, str]] = {
    "all": "всем",
    "grade_10": "десятикам",
    "grade_11": "одиннадцатым",
}
LAUNDRY_ENG_TO_RU: Final[dict[str, str]] = {
    "washing_time": "время стирки",
    "drying_time": "время сушки",
}

GRADES: Final[tuple[str, ...]] = ("10А", "10Б", "10В", "11А", "11Б", "11В")
BEAUTIFY_MEALS: Final[tuple[str, ...]] = (
    "🕗 Завтрак",
    "🕙 Второй завтрак",
    "🕐 Обед",
    "🕖 Полдник",
    "🕖 Ужин",
)
LAUNDRY_REPEAT: Final[int] = 30  # Повтор таймера прачечной через 30 минут
NOTIFIES_PER_BATCH: Final[int] = 20  # Сообщений за раз в рассылке
NO_DATA: Final[str] = "Н/д"

SLASH_COMMANDS: Final[dict[str, str]] = {
    SlashCommands.START: "Старт",
    SlashCommands.HELP: "Помощь",
    SlashCommands.SETTINGS: "Настройки",
    SlashCommands.MENU: "Меню",
}
USER_START_TEXT = """
Привет! Я - стартовое меню.
Используйте команду /menu для навигации по кнопкам

📞 <a href="https://hello.k1rles.ru/">Связь с разработчиком</a>
🐍 <a href="https://github.com/K1rL3s/Telegram-UPML-Bot">Код бота</a>
""".strip()

ADMIN_START_TEXT = """
Привет! Я - админ панель.

<b>Загрузить меню</b> - автоматическое обновление еды информацией с сайта лицея.
<b>Изменить меню</b> - ручное изменение еды.
<b>Загрузить уроки</b> - ручная загрузка изображений с расписанием уроков.
<b>Уведомление</b> - сделать оповещение.
<b>Изменить расписание воспитателей</b> - ручное изменение расписания воспитателей.
""".strip()

MAIN_MENU_TEXT = """Привет! Я - главное меню."""
