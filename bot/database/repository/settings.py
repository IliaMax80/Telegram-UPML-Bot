from typing import Any, Optional, TYPE_CHECKING

from bot.database.models.settings import Settings
from bot.database.repository.base_repo import BaseRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SettingsRepository(BaseRepository):
    """Класс для работы с настройками пользователей в базе данных."""

    def __init__(self, session: "AsyncSession") -> None:
        self.session = session

    async def get(self, user_id: int) -> "Optional[Settings]":
        """
        Возвращает Settings пользователя.

        :param user_id: ТГ Айди.
        :return: Модель Settings.
        """
        return await self._get_user_related_model(Settings, user_id)

    async def save_or_update_to_db(
        self,
        user_id: int,
        **fields: Any,
    ) -> None:
        """
        Создаёт или обновляет настройки пользователя.

        :param user_id: ТГ Айди.
        :param fields: Ключ - колонка, значение - новое значение.
        """
        if settings := await self.get(user_id):
            for k, v in fields.items():
                setattr(settings, k, v)
        else:
            settings = Settings(user_id=user_id, **fields)
            self.session.add(settings)

        await self.session.commit()
