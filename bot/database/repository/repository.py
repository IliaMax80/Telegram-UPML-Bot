import contextlib
from typing import TYPE_CHECKING, Union

from bot.utils.consts import Roles
from bot.database.repository import (
    EducatorsScheduleRepository,
    LaundryRepository,
    LessonsRepository,
    MenuRepository,
    RoleRepository,
    SettingsRepository,
    UserRepository,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class Repository:
    """Класс для вызова функций работы с базой данных."""

    def __init__(
        self,
        session: "AsyncSession",
    ) -> None:
        self.session = session
        self.user = UserRepository(session)
        self.settings = SettingsRepository(session)
        self.laundry = LaundryRepository(session)
        self.menu = MenuRepository(session)
        self.lessons = LessonsRepository(session)
        self.educators = EducatorsScheduleRepository(session)
        self.role = RoleRepository(session)

    async def save_new_user_to_db(
        self,
        user_id: int,
        username: str,
    ) -> None:
        """
        Сохранение нового пользователя или обновление никнейма существующего.

        :param user_id: ТГ Айди.
        :param username: Имя пользователя.
        """
        await self.user.save_new_to_db(user_id, username)
        await self.settings.save_or_update_to_db(user_id)
        await self.laundry.save_or_update_to_db(user_id)

    async def remove_role_from_user(
        self,
        user_id: int,
        role: "Union[Roles | str]",
    ) -> None:
        """
        Удаляет роль у юзера.

        :param user_id: ТГ Айди юзера.
        :param role: Его роль.
        """
        if isinstance(role, Roles):
            role = role.value

        user = await self.user.get(user_id)
        role = await self.role.get(role)

        with contextlib.suppress(ValueError):
            user.roles.remove(role)

        await self.session.commit()

    async def add_role_to_user(
        self,
        user_id: int,
        role: Roles | str,
    ) -> None:
        """
        Добавляет роль юзеру.

        :param user_id: ТГ Айди юзера.
        :param role: Роль.
        """
        if isinstance(role, Roles):
            role = role.value

        user = await self.user.get(user_id)
        role = await self.role.get(role)

        user.roles.append(role)

        await self.session.commit()
