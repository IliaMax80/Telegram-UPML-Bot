import datetime as dt

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.utils.consts import AdminCallback, TextCommands, UserCallback
from bot.utils.datehelp import date_today, format_date


go_to_main_menu_button = InlineKeyboardButton(
    text="🏠Главное меню",
    callback_data=UserCallback.OPEN_MAIN_MENU,
)

go_to_settings_button = InlineKeyboardButton(
    text=TextCommands.SETTINGS,
    callback_data=UserCallback.OPEN_SETTINGS,
)

go_to_admin_panel_button = InlineKeyboardButton(
    text=TextCommands.ADMIN_PANEL,
    callback_data=AdminCallback.OPEN_ADMIN_PANEL,
)

cancel_state_button = InlineKeyboardButton(
    text="❌Отмена",
    callback_data=UserCallback.CANCEL_STATE,
)

cancel_state_keyboard = InlineKeyboardMarkup(inline_keyboard=[[cancel_state_button]])


def _keyboard_for_left_right_menu(
    open_smt_on_callback: str,
    open_smt_today_callback: str,
    today_smile: str,
    curr_date: "dt.date" = None,
) -> "InlineKeyboardMarkup":
    """Клавиатура для меню с навигацией влево-вправо по датам.

    :param open_smt_on_callback: Строка формата "open_{smt}_on_{date}".
    :param open_smt_today_callback: Строка формата "open_{smt}_on_today".
    :param today_smile: Смайлик на кнопке "Сегодня".
    :param curr_date: Дата, на которой открыта навигация. None - сегодня.
    :return: Клавиатура меню навигации влево-вправо.
    """
    today = date_today()

    if curr_date is None:
        curr_date = today

    tomorrow = curr_date + dt.timedelta(days=1)
    yesterday = curr_date - dt.timedelta(days=1)
    tomorrow_str = format_date(tomorrow)
    yesterday_str = format_date(yesterday)

    keyboard = InlineKeyboardBuilder()

    if abs((today - yesterday).days) < 7:
        keyboard.add(
            InlineKeyboardButton(
                text=f"⬅️{yesterday_str}",
                callback_data=open_smt_on_callback + yesterday_str,
            ),
        )

    keyboard.add(
        InlineKeyboardButton(
            text=f"{today_smile}Сегодня",
            callback_data=open_smt_today_callback,
        ),
    )

    if abs((today - tomorrow).days) < 7:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{tomorrow_str}➡️",
                callback_data=open_smt_on_callback + tomorrow_str,
            ),
        )

    keyboard.row(go_to_main_menu_button)

    return keyboard.as_markup()
