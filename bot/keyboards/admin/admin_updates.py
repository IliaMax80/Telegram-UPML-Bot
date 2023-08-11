from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from bot.keyboards.universal import cancel_state_button
from bot.utils.consts import CallbackData


choose_meal_keyboard = InlineKeyboardBuilder().add(
    *[
        InlineKeyboardButton(text=dish, callback_data=callback_data)
        for dish, callback_data in zip(
            ('🕗Завтрак', '🕙Второй завтрак',
             '🕐Обед', '🕖Полдник',
             '🕖Ужин'),
            (CallbackData.EDIT_BREAKFAST, CallbackData.EDIT_LUNCH,
             CallbackData.EDIT_DINNER, CallbackData.EDIT_SNACK,
             CallbackData.EDIT_SUPPER)
        )
    ],
    cancel_state_button
).adjust(3, 2, 1).as_markup()

confirm_edit_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='✅Подтвердить',
                callback_data=CallbackData.EDIT_CONFIRM
            ),
            cancel_state_button
        ]
    ]
)
