import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot.database.repository.repository import Repository
from bot.funcs.client.laundry import laundry_cancel_timer_func
from bot.keyboards import laundry_keyboard
from bot.utils.consts import LAUNDRY_REPEAT
from bot.utils.datehelp import datetime_now
from bot.utils.notify import one_notify

if TYPE_CHECKING:
    from aiogram import Bot


LAUNDRY_TIMER_EXPIRED = "🔔Таймер прачечной вышел! ({0})".format


async def check_laundry_timers(
    bot: "Bot",
    session_maker: "async_sessionmaker[AsyncSession]",
) -> None:
    """Делатель уведомлений для истёкших таймеров прачечной."""
    async with session_maker() as session:
        repo = Repository(session)
        for laundry in await repo.laundry.get_expired():
            rings = laundry.rings or 0

            result = await one_notify(
                bot,
                repo.user,
                laundry.user,
                LAUNDRY_TIMER_EXPIRED(rings + 1),
                await laundry_keyboard(laundry, rings < 2),
            )
            if not result or rings >= 2:
                await laundry_cancel_timer_func(repo.laundry, laundry.user.user_id)
            else:
                now = datetime_now()
                await repo.laundry.save_or_update_to_db(
                    laundry.user.user_id,
                    rings=rings + 1,
                    start_time=now,
                    end_time=now + dt.timedelta(minutes=LAUNDRY_REPEAT),
                )
