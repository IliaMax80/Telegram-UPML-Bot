YES = "✅"
NO = "❌"
QUESTION = "❓"
NO_DATA = "Н/д"

USER_START_TEXT = """
Привет! Я - стартовое меню.
Используйте команду /menu для навигации по кнопкам

📞 <a href="https://hello.k1rles.ru/">Связь с разработчиком</a>
🐍 <a href="https://github.com/K1rL3s/Telegram-UPML-Bot">Код бота</a>
""".strip()

SETTINGS_WELCOME_TEXT = """
Привет! Я - настройки!

<b>Класс</b> - твой класс.
<b>Уроки</b> - уведомления при изменении расписания.
<b>Новости</b> - уведомления о мероприятиях, новостях.
<b>Стирка</b> - время таймера для стирки.
<b>Сушка</b> - время таймера для сушки.
""".strip()

ADMIN_START_TEXT = """
Привет! Я - админ панель.

<b>Загрузить меню</b> - автоматическое обновление еды информацией с сайта лицея.
<b>Изменить меню</b> - ручное изменение еды.
<b>Загрузить уроки</b> - ручная загрузка изображений с расписанием уроков.
<b>Уведомление</b> - сделать оповещение.
<b>Изменить расписание воспитателей</b> - ручное изменение расписания воспитателей.
""".strip()

MAIN_MENU_TEXT = "Привет! Я - главное меню."


SET_TIMER_TEXT = (
    "🕛 Чтобы установить таймер на срабатывание через какое-то время, "
    "введите часы и минуты через точку, запятую или пробел "
    "<i>(0.30, 1 0, 12,45)</i>.\n"
    "⏰ Чтобы установить таймер на срабатывание в какое-то время, "
    "введите это время через двоеточие <i>(12:30, 16:00, 19:50)</i>"
)

DONT_UNDERSTAND_DATE = (
    f"{NO} Не понял это как дату, попробуйте ещё раз. Формат - <b>ДД.ММ.ГГГГ</b>"
)
DONT_UNDERSTAND_TIMER = (
    f"{NO} Не понял это как часы и минуты. Попробуйте ещё раз.\n\n{SET_TIMER_TEXT}"
)
