from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.database.db_funcs import get_laundry
from src.keyboards.universal import (
    go_to_main_menu_button,
    go_to_settings_button,
)
from src.utils.consts import CallbackData


def laundry_keyboard(
        user_id: int,
        add_cancel_if_timer: bool = True
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            '🏖Запустить стирку',
            callback_data=CallbackData.START_WASHING_TIMER
        ),
        InlineKeyboardButton(
            '💨Запустить сушку',
            callback_data=CallbackData.START_DRYING_TIMER
        )
    )

    if add_cancel_if_timer and get_laundry(user_id).is_active:
        keyboard.add(
            InlineKeyboardButton(
                '❌Отменить таймер',
                callback_data=CallbackData.CANCEL_LAUNDRY_TIMER
            )
        )

    keyboard.add(
        go_to_main_menu_button,
        go_to_settings_button
    )

    return keyboard
