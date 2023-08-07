from datetime import date

from src.database.db_funcs import (
    get_settings, get_full_lessons,
    get_class_lessons,
)
from src.utils.datehelp import format_date, weekday_by_date


async def get_lessons_text_and_image_id(
        user_id: int,
        lesson_date: date = None
) -> tuple[str, list[str] | None]:
    """
    Возвращает сообщение для пользователя и:
    Если класс выбран, то список из двух
        айди с расписанием паралелли и выбранного класса.
    Если класс не выбран, то список из двух
        айди с расписаниями параллелей.
    Если расписаний нет, то None.

    :param user_id: Айди юзера.
    :param lesson_date: Дата расписания.
    :return: Сообщение и список с двумя айди изображений.
    """

    settings = await get_settings(user_id)

    images = []

    if settings.class_:
        images.append(await get_full_lessons(lesson_date, settings.grade))
        images.append(await get_class_lessons(lesson_date, settings.class_))
    else:
        images.append(await get_full_lessons(lesson_date, "10"))
        images.append(await get_full_lessons(lesson_date, "11"))

    for_class = settings.class_ if settings.class_ else "❓"

    if any(images):
        text = f'✏ Расписание на *{format_date(lesson_date)}* ' \
               f'({weekday_by_date(lesson_date)}) для *{for_class}* класса.'
    else:
        images = None
        text = f'🛏 Расписание на *{format_date(lesson_date)}* ' \
               f'({weekday_by_date(lesson_date)}) ' \
               f'для *{for_class}* класса не найдено :(.'

    return text, images
