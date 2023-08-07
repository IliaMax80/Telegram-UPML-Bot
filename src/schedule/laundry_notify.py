from datetime import timedelta

from aiogram import Bot

from src.database.db_funcs import get_expired_laundries, save_or_update_laundry
from src.handlers.laundry import laundry_cancel_timer_handler
from src.keyboards import laundry_keyboard
from src.utils.consts import LAUNDRY_REPEAT
from src.utils.datehelp import datetime_now
from src.utils.funcs import one_notify


async def check_laundry_timers(bot: Bot) -> None:
    """
    Делатель уведомлений для истёкших таймеров прачки.
    """
    for laundry in await get_expired_laundries():
        laundry.rings = laundry.rings or 0

        result = await one_notify(
            f'🔔Таймер прачечной вышел! ({laundry.rings + 1})',
            laundry.user,
            bot,
            await laundry_keyboard(laundry.user.user_id, laundry.rings < 2)
        )
        if not result:
            continue

        if laundry.rings >= 2:
            await laundry_cancel_timer_handler(laundry.user.user_id)
        else:
            now = datetime_now()
            await save_or_update_laundry(
                laundry.user.user_id,
                rings=laundry.rings + 1, start_time=now,
                end_time=now + timedelta(minutes=LAUNDRY_REPEAT)
            )
