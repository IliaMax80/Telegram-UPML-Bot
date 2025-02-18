from typing import Optional, TYPE_CHECKING, Union

from sqlalchemy import select

from bot.database.models.class_lessons import ClassLessons
from bot.database.models.full_lessons import FullLessons
from bot.database.repository.base_repo import BaseRepository

if TYPE_CHECKING:
    import datetime as dt

    from sqlalchemy.ext.asyncio import AsyncSession


class LessonsRepository(BaseRepository):
    """Класс для работы с расписаниями уроков в базе данных."""

    def __init__(self, session: "AsyncSession") -> None:
        self.session = session

    async def get(
        self,
        lessons_date: "dt.date",
        class_or_grade: str,
    ) -> "Union[ClassLessons, FullLessons, None]":
        """
        Возвращает модель с айди изображением уроков на дату.

        :param lessons_date: Дата.
        :param class_or_grade: Класс в формате "10Б" или только паралелль (10 или 11).
        :return: Модель ClassLessons или FullLessons.
        """
        if class_or_grade.isdigit():
            return await self._get_full_lessons(lessons_date, class_or_grade)
        return await self._get_class_lessons(lessons_date, class_or_grade)

    async def save_or_update_to_db(
        self,
        image: str,
        lessons_date: "dt.date",
        grade: str,
        letter: str = None,
    ) -> None:
        """
        Сохраняет или обновляет уроки для паралелли.

        :param image: Айди изображения.
        :param lessons_date: Дата.
        :param grade: 10 или 11.
        :param letter: А, Б, В
        """
        model = ClassLessons if letter else FullLessons

        find_query = select(model).where(
            model.date == lessons_date,
            model.grade == grade,
        )

        if letter:
            find_query = find_query.where(model.letter == letter)

        if lessons := await self.session.scalar(find_query):
            lessons.image = image
        else:
            data = {
                "date": lessons_date,
                "grade": grade,
                "image": image,
            }
            if letter:
                data["letter"] = letter
            lessons = model(**data)
            self.session.add(lessons)

        await self.session.commit()

    async def _get_class_lessons(
        self,
        lessons_date: "dt.date",
        class_: str,
    ) -> "Optional[ClassLessons]":
        """
        Возвращает айди картинки расписания уроков для класса.

        :param lessons_date: Дата.
        :param class_: (10 или 11) + (А или Б или В) | (10А, 11Б, ...)
        :return: Айди картинки или None.
        """
        query = select(ClassLessons).where(
            ClassLessons.date == lessons_date,
            ClassLessons.class_ == class_,
        )
        return await self.session.scalar(query)

    async def _get_full_lessons(
        self,
        lessons_date: "dt.date",
        grade: str,
    ) -> "Optional[FullLessons]":
        """
        Возвращает айди картинки расписания уроков для параллели.

        :param lessons_date: Дата.
        :param grade: 10 или 11.
        :return: Айди картинки или None.
        """
        query = select(FullLessons).where(
            FullLessons.date == lessons_date,
            FullLessons.grade == grade,
        )
        return await self.session.scalar(query)
