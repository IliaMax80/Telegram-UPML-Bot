from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.database.db_funcs import is_has_any_role
from src.keyboards.admin.admin_manage import open_admins_list_button
from src.keyboards.universal import go_to_main_menu_button
from src.utils.consts import CallbackData, Roles


def admin_panel_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    for button_text, callback_data in zip(
        ('🍴Загрузить меню', '🍴Изменить меню',
         '📓Загрузить уроки', '🔔Уведомление'),
        (CallbackData.AUTO_UPDATE_CAFE_MENU,
         CallbackData.EDIT_CAFE_MENU,
         CallbackData.UPLOAD_LESSONS, CallbackData.DO_A_NOTIFY_FOR_)
    ):
        keyboard.insert(
            InlineKeyboardButton(button_text, callback_data=callback_data)
        )

    if is_has_any_role(user_id, [Roles.SUPERADMIN]):
        keyboard.add(open_admins_list_button)

    keyboard.add(go_to_main_menu_button)

    return keyboard
