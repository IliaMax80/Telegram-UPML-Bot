from typing import TYPE_CHECKING

from aiogram import F, Router
from aiogram.filters import Command

from bot.keyboards import main_menu_inline_keyboard
from bot.utils.consts import SlashCommands, TextCommands, UserCallback

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery, Message

    from bot.database.repository.repository import Repository


router = Router(name=__name__)


@router.callback_query(F.data == UserCallback.OPEN_ELECTIVES)
async def electives_callback_handler(
    callback: "CallbackQuery",
) -> None:
    """Обработчик кнопки "Элективы"."""
    await callback.message.edit_text(
        text="🥲",
        reply_markup=callback.message.reply_markup,
    )


@router.message(F.text == TextCommands.ELECTIVES)
@router.message(Command(SlashCommands.ELECTIVES))
async def electives_message_handler(
    message: "Message",
    repo: "Repository",
) -> None:
    """Обработчик команды "/electives"."""
    await message.answer(
        text="🥲",
        reply_markup=await main_menu_inline_keyboard(repo, message.from_user.id),
    )
