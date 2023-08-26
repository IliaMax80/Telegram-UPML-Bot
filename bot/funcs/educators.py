from typing import TYPE_CHECKING

from bot.utils.consts import NO_DATA
from bot.utils.datehelp import date_today, format_date, weekday_by_date

if TYPE_CHECKING:
    import datetime as dt

    from bot.database.repository.repository import Repository


async def get_format_educators_by_date(
    repo: "Repository",
    schedule_date: "dt.date" = None,
) -> str:
    """Возвращает расписание воспитателей по дате.

    Н/д, если данных нет.

    :param repo: Доступ к базе данных.
    :param schedule_date: Нужная дата.
    :return: Готовое сообщение для телеги.
    """
    if schedule_date is None:
        schedule_date = date_today()

    schedule = await repo.educators.get(schedule_date)

    return (
        f"😵 <b>Воспитатели на {format_date(schedule_date)} "
        f"({weekday_by_date(schedule_date)})</b>:\n\n"
        f"{getattr(schedule, 'schedule', None) or NO_DATA}"
    )
