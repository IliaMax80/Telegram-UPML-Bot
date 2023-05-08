from datetime import date, timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils.consts import CallbackData
from src.utils.dateformat import format_date


go_to_main_menu_button = InlineKeyboardButton(
    "🏠Главное меню",
    callback_data=CallbackData.OPEN_MAIN_MENU
)


def _get_keyboard_for_left_right_menu(
        open_smt_on_callback: str,
        open_smt_today_callback: str,
        today_smile: str,
        curr_date: date = None,
) -> InlineKeyboardMarkup:

    today = date.today()

    if curr_date is None:
        curr_date = date.today()

    tomorrow = curr_date + timedelta(days=1)
    yesterday = curr_date - timedelta(days=1)
    tomorrow_str = format_date(tomorrow)
    yesterday_str = format_date(yesterday)

    keyboard = InlineKeyboardMarkup()

    if abs((today - yesterday).days) < 7:
        keyboard.insert(
            InlineKeyboardButton(
                f'⬅️{yesterday_str}',
                callback_data=open_smt_on_callback + yesterday_str
            )
        )

    keyboard.insert(
        InlineKeyboardButton(
            f'{today_smile}Сегодня',
            callback_data=open_smt_today_callback
        )
    )

    if abs((today - tomorrow).days) < 7:
        keyboard.insert(
            InlineKeyboardButton(
                f'➡️{tomorrow_str}',
                callback_data=open_smt_on_callback + tomorrow_str
            )
        )

    keyboard.row(
        go_to_main_menu_button
    )

    return keyboard
