from typing import TYPE_CHECKING

from bot.keyboards.universal import _keyboard_for_left_right_menu
from bot.utils.enums import UserCallback


if TYPE_CHECKING:
    import datetime as dt

    from aiogram.types import InlineKeyboardMarkup


def educators_keyboard(date: "dt.date" = None) -> "InlineKeyboardMarkup":
    """Клавиатура для расписания воспитателей с перемоткой влево-вправо по дням."""
    return _keyboard_for_left_right_menu(
        open_smt_on_=UserCallback.OPEN_EDUCATORS_ON_,
        today_smile="👩‍✈️",
        date=date,
    )
