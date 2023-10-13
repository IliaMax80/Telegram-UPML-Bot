from typing import TYPE_CHECKING

from bot.keyboards.universal import _left_right_keyboard_navigation
from bot.utils.enums import UserCallback


if TYPE_CHECKING:
    import datetime as dt

    from aiogram.types import InlineKeyboardMarkup


def educators_keyboard(date: "dt.date" = None) -> "InlineKeyboardMarkup":
    """Клавиатура для расписания воспитателей с перемоткой влево-вправо по дням."""
    return _left_right_keyboard_navigation(
        menu=UserCallback.EDUCATORS,
        today_smile="👩‍✈️",
        date=date,
    )
