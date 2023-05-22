from datetime import timedelta

from src.database.db_funcs import get_expired_laundries, save_or_update_laundry
from src.handlers.laundry import laundry_cancel_timer_handler
from src.keyboards import laundry_keyboard
from src.utils.consts import LAUNDRY_REPEAT
from src.utils.datehelp import datetime_now
from src.utils.funcs import one_notify


async def check_laundry_timers() -> None:
    """
    Делатель уведомлений для истёкших таймеров прачки.
    """
    for laundry in get_expired_laundries():
        result = await one_notify(
            f'🔔Таймер прачечной вышел! ({(laundry.rings or 0) + 1})',
            laundry.user,
            laundry_keyboard(laundry.user.user_id, (laundry.rings or 0) < 2)
        )
        if result:
            if (laundry.rings or 0) >= 2:
                laundry_cancel_timer_handler(laundry.user.user_id)
            else:
                now = datetime_now()
                save_or_update_laundry(
                    laundry.user.user_id,
                    rings=(laundry.rings or 0) + 1, start_time=now,
                    end_time=now + timedelta(minutes=LAUNDRY_REPEAT)
                )
