from aiogram import F, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from bot.database.db_funcs import Repository
from bot.filters import IsAdmin, SaveUser
from bot.keyboards import (
    go_to_main_menu_keyboard, main_menu_keyboard, admin_panel_keyboard,
)
from bot.utils.consts import CallbackData, SlashCommands, TextCommands


router = Router(name=__name__)


@router.message(F.text == TextCommands.START, SaveUser())
@router.message(Command(SlashCommands.START), SaveUser())
async def start_handler(message: types.Message) -> None:
    """
    Обработчик команды "/start".
    """
    text = 'Привет! Я - стартовое меню.'

    await message.reply(
        text=text,
        reply_markup=go_to_main_menu_keyboard
    )


@router.message(F.text == TextCommands.MENU, SaveUser())
@router.callback_query(F.data == CallbackData.OPEN_MAIN_MENU, SaveUser())  #
async def main_menu_handler(
        message: types.Message | types.CallbackQuery,
        repo: Repository,
) -> None:
    """
    Обработчик команды "/menu" и кнопки "Главное меню".
    """
    text = 'Привет! Я - главное меню.'
    keyboard = await main_menu_keyboard(repo, message.from_user.id)

    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
    else:
        await message.reply(
            text=text,
            reply_markup=keyboard
        )


@router.message(F.text == TextCommands.HELP, SaveUser())
@router.message(Command(SlashCommands.HELP), SaveUser())
async def help_handler(message: types.Message) -> None:
    """
    Обработчик команды "/help".
    """
    await message.reply('Помощь!')


@router.callback_query(F.data == CallbackData.OPEN_ADMIN_PANEL, IsAdmin())
async def admin_panel_handler(
        callback: types.CallbackQuery,
        repo: Repository,
) -> None:
    """
    Обработчик кнопки "Админ панель".
    """
    text = """
Привет! Я - админ панель.

*Загрузить меню* - автоматическое обновление еды информацией с сайта лицея.
*Изменить меню* - ручное изменение еды.
*Загрузить уроки* - ручная загрузка изображений с расписанием уроков.
*Уведомление* - сделать оповещение.
""".strip()
    keyboard = await admin_panel_keyboard(repo, callback.from_user.id)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@router.message(F.text == TextCommands.CANCEL, StateFilter('*'))
@router.message(
    Command(SlashCommands.CANCEL, SlashCommands.STOP), StateFilter('*')
)
@router.callback_query(F.data == CallbackData.CANCEL_STATE, StateFilter('*'))
async def cancel_state(
        message: types.Message | types.CallbackQuery,
        state: FSMContext,
        repo: Repository,
) -> None:
    """
    Обработчик кнопок с отменой состояний и команд "/cancel", "/stop".
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await main_menu_handler(message, repo)
