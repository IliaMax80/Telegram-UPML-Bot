import datetime as dt
from typing import Optional, Union

from bot.settings import get_settings
from bot.utils.consts import TODAY


# Смещение часового пояса по умолчанию, используется при работе бота.
# В тестах всегда должно подставляться одинаковое значение.
default_timezone_offset = get_settings().other.timezone_offset


def format_date(date: "dt.date", with_year: bool = True) -> str:
    """
    Формат объекта даты в вид "dd.MM.YYYY" с лидирующими нулями.

    :param date: Объект даты.
    :param with_year: Вернуть строку годом или без.
    :return: Отформатированная строка.
    """
    return date.strftime("%d.%m.%Y") if with_year else date.strftime("%d.%m")


def format_datetime(datetime: "dt.datetime") -> str:
    """
    Формат объекта даты и времени в вид "dd.MM.YYYY hh:mm:ss" с лидирующими нулями.

    :param datetime: Объект даты и времени.
    :return: Отформатированная строка.
    """
    return datetime.strftime("%d.%m.%Y %H:%M:%S")


def date_by_format(
    date: str,
    timezone_offset: int | float = default_timezone_offset,
) -> "Union[dt.date, bool]":
    """
    Конвертация отформатированной строки в дату.

    :param date: Дата в виде строки, день-месяц-год через тире, точку или пробел.
    :param timezone_offset: Смещение часового пояса в часах.
    :return: Объект даты.
    """
    if date.lower() == TODAY:
        return date_today(timezone_offset)

    date = date.replace("-", " ").replace(".", " ")
    try:
        day, month, year = map(int, date.strip().split())

        if year < 1000:  # Если не ГГГГ, а ГГ
            year += date_today().year // 1000 * 1000

        date_obj = dt.date(day=day, month=month, year=year)
    except ValueError:
        return False
    return date_obj


def time_by_format(time: str) -> "Union[dt.time, bool]":
    """
    Конвертация строки формата "{часы}:{минуты}" в объект времени.

    :param time: Время в виде строки, где часы и минуты разделены двоеточием.
    :return: Объект времени.
    """
    hours, minutes = map(int, time.split(":"))
    return dt.time(hour=hours, minute=minutes)


def format_time(time: "Union[dt.time, dt.datetime]") -> str:
    """
    Формат объекта времени в вид "HH:MM" с лидирующими нулями.

    :param time: Объект времени.
    :return: Отформатированная строка.
    """
    return time.strftime("%H:%M")


def datetime_time_delta(datetime: "dt.datetime", time: "dt.time") -> "dt.timedelta":
    """
    Возвращает разницу между временем из объекта datetime и переданным временем.

    :param datetime: Объект datetime, с которым нужно сравнить время.
    :param time: Целевое время для сравнения.
    :return: timedelta объект, представляющий разницу во времени.
    """
    datetime_time = datetime.time()

    timedelta = dt.timedelta(
        hours=time.hour,
        minutes=time.minute,
    ) - dt.timedelta(
        hours=datetime_time.hour,
        minutes=datetime_time.minute,
    )

    if timedelta.total_seconds() < 0:
        timedelta += dt.timedelta(hours=24)

    return timedelta


def hours_minutes_to_minutes(text: str) -> int:
    """
    Строка формата "{часы} {минуты}" в минуты, разделитель точка, запятая или пробел.

    :param text: Сообщение пользователя.
    :return: Минуты.
    """
    hours, minutes = map(int, text.replace(",", " ").replace(".", " ").split())
    return hours * 60 + minutes


def minutes_to_hours_minutes(minutes: int) -> tuple[int, int]:
    """
    Конвертация минут в часы и минуты.

    :param minutes: Минуты.
    :return: Часы и минуты.
    """
    if minutes < 0:
        raise ValueError("minutes must be greater than or equal to 0")
    return minutes // 60, minutes % 60


def weekday_by_date(date: "dt.date") -> str:
    """
    День недели по дате.

    :param date: Объект даты.
    :return: День недели в виде строки.
    """
    return (
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "воскресенье",
    )[date.weekday()]


def get_monday_of_week(
    date: "Optional[dt.date]" = None,
    timezone_offset: int | float = default_timezone_offset,
) -> "dt.date":
    """
    Возвращает объект date с понедельником недели.

    :param date: Дата, понедельник недели которой надо вернуть.
    :param timezone_offset: Смещение часового пояса в часах.
    :return: date.
    """
    if date is None:
        date = date_today(timezone_offset)
    return date - dt.timedelta(days=date.weekday())


def datetime_now(
    timezone_offset: int | float = default_timezone_offset,
) -> "dt.datetime":
    """
    Функция datetime.datetime.now, но в указанной в ``.env`` временной зоне.

    :param timezone_offset: Смещение часового пояса в часах.
    :return: datetime.
    """
    return dt.datetime.now(
        tz=dt.timezone(offset=dt.timedelta(hours=timezone_offset)),
    ).replace(tzinfo=None)


def date_today(timezone_offset: int | float = default_timezone_offset) -> "dt.date":
    """
    Функция datetime.date.today, но в указанной в ``.env`` временной зоне.

    :param timezone_offset: Смещение часового пояса в часах.
    :return: date.
    """
    return datetime_now(timezone_offset).date()
