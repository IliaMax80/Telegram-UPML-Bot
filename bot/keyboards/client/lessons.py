from typing import TYPE_CHECKING

from bot.keyboards.universal import _keyboard_for_left_right_menu
from bot.utils.consts import UserCallback

if TYPE_CHECKING:
    import datetime as dt

    from aiogram.types import InlineKeyboardMarkup


def lessons_keyboard(curr_date: "dt.date" = None) -> "InlineKeyboardMarkup":
    """Клавиатура для расписания уроков с перемоткой влево-вправо по дня."""
    return _keyboard_for_left_right_menu(
        open_smt_on_callback=UserCallback.OPEN_LESSONS_ON_,
        open_smt_today_callback=UserCallback.OPEN_LESSONS_TODAY,
        today_smile="📓",
        curr_date=curr_date,
    )
