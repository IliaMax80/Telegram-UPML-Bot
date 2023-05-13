from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.keyboards.universal import (
    cancel_state_button,
    go_to_admin_panel_button,
)
from src.utils.consts import CallbackData


open_admins_list_button = InlineKeyboardButton(
    '👮‍♀️Список админов',
    callback_data=CallbackData.OPEN_ADMINS_LIST_PAGE_
)
add_new_admin_button = InlineKeyboardButton(
    '🔎Добавить админа',
    callback_data=CallbackData.ADD_NEW_ADMIN
)
add_new_admin_sure_keyboard = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        '✅Подтвердить',
        callback_data=CallbackData.ADD_NEW_ADMIN_SURE
    ),
    cancel_state_button
)


def admins_list_keyboard(
        users: list[tuple[str, int]],
        page: int
) -> InlineKeyboardMarkup:
    upp = 6  # 6 пользователей на страницу (users per page)
    keyboard = InlineKeyboardMarkup(row_width=2)

    for name, user_id in users[page * upp:page * upp + upp]:
        keyboard.insert(
            InlineKeyboardButton(
                name,
                callback_data=CallbackData.CHECK_ADMIN_ + f'{user_id}_{page}'
            )
        )

    if page > 0:
        keyboard.add(
            InlineKeyboardButton(
                f'⬅️Назад',
                callback_data=
                CallbackData.OPEN_ADMINS_LIST_PAGE_ + f'{page - 1}'
            )
        )

    if page * upp + upp < len(users):
        keyboard.insert(
            InlineKeyboardButton(
                f'➡️Вперёд',
                callback_data=
                CallbackData.OPEN_ADMINS_LIST_PAGE_ + f'{page + 1}'
            )
        )

    keyboard.add(
        go_to_admin_panel_button,
        add_new_admin_button
    )

    return keyboard


def check_admin_keyboard(
        user_id: int,
        page: int,
        sure: bool = False
) -> InlineKeyboardMarkup:
    remove_button = InlineKeyboardButton(
        "🚫Точно снять роль" if sure else "🚫Снять роль админа",
        callback_data=(
            CallbackData.REMOVE_ADMIN_SURE_ + f'{user_id}'
            if sure else
            CallbackData.REMOVE_ADMIN_ + f'{user_id}_{page}'
        )
    )
    return InlineKeyboardMarkup().add(
        remove_button
    ).add(
        go_to_admin_panel_button,
        InlineKeyboardButton(
            f'👨‍✈️Список админов',
            callback_data=CallbackData.OPEN_ADMINS_LIST_PAGE_ + f'{page}'
        )
    )
