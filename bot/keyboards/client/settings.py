from typing import TYPE_CHECKING

from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


from bot.keyboards.universal import go_to_main_menu_button
from bot.utils.consts import GRADES, UserCallback

if TYPE_CHECKING:
    from bot.database.models.settings import Settings


async def settings_keyboard(settings: "Settings") -> "InlineKeyboardMarkup":
    """Клавиатура настроек, своя у каждого пользователя."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Класс " + (settings.class_ if settings.class_ else "❓"),
                    callback_data=UserCallback.CHANGE_GRADE_TO_,
                ),
                InlineKeyboardButton(
                    text="Уроки " + ("✅" if settings.lessons_notify else "❌"),
                    callback_data=UserCallback.SWITCH_LESSONS_NOTIFY,
                ),
                InlineKeyboardButton(
                    text="Новости " + ("✅" if settings.news_notify else "❌"),
                    callback_data=UserCallback.SWITCH_NEWS_NOTIFY,
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"⏳Стирка {settings.washing_time} мин.",
                    callback_data=UserCallback.EDIT_WASHING_TIME,
                ),
                InlineKeyboardButton(
                    text=f"💨Сушка {settings.drying_time} мин.",
                    callback_data=UserCallback.EDIT_DRYING_TIME,
                ),
            ],
            [go_to_main_menu_button],
        ],
    )


choose_grade_keyboard = (
    InlineKeyboardBuilder()
    .add(
        *(
            InlineKeyboardButton(
                text=f"{grade_letter}",
                callback_data=UserCallback.CHANGE_GRADE_TO_ + grade_letter,
            )
            for grade_letter in GRADES
        ),
        InlineKeyboardButton(
            text="⏪Настройки",
            callback_data=UserCallback.OPEN_SETTINGS,
        ),
        InlineKeyboardButton(
            text="❓Сбросить класс",
            callback_data=UserCallback.CHANGE_GRADE_TO_ + "None",
        ),
    )
    .adjust(3, 3, 2)
    .as_markup()
)
