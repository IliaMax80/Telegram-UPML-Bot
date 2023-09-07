import datetime as dt
from io import BytesIO
from typing import TYPE_CHECKING

from loguru import logger

from bot.custom_types import Album, LessonsImage
from bot.upml.process_lessons import process_one_lessons_file
from bot.utils.datehelp import format_date
from bot.utils.funcs import bytes_io_to_image_id

if TYPE_CHECKING:
    from aiogram import Bot

    from bot.database.repository import LessonsRepository


async def tesseract_album_lessons_func(
    bot: "Bot",
    repo: "LessonsRepository",
    chat_id: int,
    album: "Album",
    tesseract_path: str,
) -> list[LessonsImage]:
    """
    Приниматель альбома для поочерёдной обработки каждой фотографии расписания.

    :param album: Альбом с фотографиями расписаний.
    :param chat_id: Откуда пришёл альбом с расписаниями.
    :param tesseract_path: Путь до exeшника тессеракта.
    :param bot: Текущий ТГ Бот.
    :param repo: Репозиторий расписаний уроков.
    :return: Склейка итогов обработки расписаний.
    """
    results: list[LessonsImage] = []

    for photo in album.photo:
        photo_id = photo.file_id
        photo = await bot.get_file(photo_id)
        await bot.download_file(photo.file_path, image := BytesIO())

        result = await _tesseract_one_lessons_func(
            bot,
            repo,
            chat_id,
            image,
            tesseract_path,
        )

        if isinstance(result, tuple):
            grade, date = result
            results.append(
                LessonsImage(
                    text=(
                        f"Расписание для <b>{grade}-х классов</b> "
                        f"на <b>{format_date(date)}</b> сохранено!"
                    ),
                    status=True,
                    photo_id=photo_id,
                    grade=grade,
                    date=date,
                ),
            )
        else:
            results.append(
                LessonsImage(
                    text=result,
                    status=False,
                    photo_id=photo_id,
                    grade=None,
                    date=None,
                ),
            )

    return results


async def _tesseract_one_lessons_func(
    bot: "Bot",
    repo: "LessonsRepository",
    chat_id: int,
    image: "BytesIO",
    tesseract_path: str,
) -> tuple[str, "dt.date"] | str:
    """
    Передача расписания в обработчик и сохранение результата в базу данных.

    :param chat_id: Айди чата, откуда пришло изображение с расписанием.
    :param image: Изображение с расписанием.
    :param tesseract_path: Путь до exeшника тессеракта.
    :param bot: ТГ Бот.
    :param repo: Репозиторий расписаний уроков.
    :return: Паралелль и дата, если окей, иначе текст ошибки.
    """
    try:
        date, grade, full_lessons, class_lessons = process_one_lessons_file(
            image,
            tesseract_path,
        )
    except ValueError as e:
        logger.warning(text := f"Ошибка при загрузке расписания: {repr(e)}")
        return text

    full_lessons_id = await bytes_io_to_image_id(chat_id, image, bot)
    class_lessons_ids = [
        await bytes_io_to_image_id(chat_id, class_image, bot)
        for class_image in class_lessons
    ]

    await save_lessons_to_db_func(
        repo,
        LessonsImage(
            text=None,
            status=True,
            photo_id=full_lessons_id,
            grade=grade,
            date=date,
        ),
        [
            LessonsImage(
                text=None,
                status=True,
                photo_id=class_id,
                grade=grade,
                date=date,
            )
            for class_id in class_lessons_ids
        ],
    )

    return grade, date


async def save_lessons_to_db_func(
    repo: "LessonsRepository",
    full_lessons: "LessonsImage",
    class_lessons: "list[LessonsImage]",
) -> None:
    """
    Сохранение готовых изображений расписаний уроков на дату для параллели.

    :param repo: Репозиторий расписаний уроков.
    :param full_lessons: Полное изображение расписания уроков.
    :param class_lessons: Обрезанные изображения расписания уроков по буквам классов.
    """
    await repo.save_or_update_to_db(
        full_lessons.photo_id,
        full_lessons.date,
        full_lessons.grade,
    )
    for class_lesson, letter in zip(class_lessons, "АБВ"):
        class_lesson: LessonsImage
        await repo.save_or_update_to_db(
            class_lesson.photo_id,
            class_lesson.date,
            class_lesson.grade,
            letter,
        )
