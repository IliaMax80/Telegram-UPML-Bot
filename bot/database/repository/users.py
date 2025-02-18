from enum import Enum
from typing import Any, Optional, TYPE_CHECKING, Union

from loguru import logger
import sqlalchemy as sa

from sqlalchemy.orm import Mapped, MappedColumn, selectinload

from bot.database.models.roles import Role
from bot.database.models.settings import Settings
from bot.database.models.users import User
from bot.database.repository.base_repo import BaseRepository


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from bot.utils.consts import Roles


class UserRepository(BaseRepository):
    """Класс для работы с пользователями в базе данных."""

    def __init__(self, session: "AsyncSession") -> None:
        self.session = session

    async def get(self, user_id: int) -> "Optional[User]":
        """
        Возвращает пользователя.

        :param user_id: ТГ Айди.
        :return: Модель User.
        """
        return await self._get_user_related_model(User, user_id)

    async def get_by_conditions(
        self,
        values: "list[tuple[Union[MappedColumn, Mapped], Any]]",
        or_mode: bool = False,
    ) -> list["User"]:
        """
        Cписок Userов, у которых значение в Settings или User совпадает с переданным.

        :param values: Список из кортежей,
                       где первый элемент - колонка таблицы, второй - значение.
                       Пустой список - все юзеры.
        :param or_mode: Если True, то совпадение хотя бы по одному условию.
        :return: Список юзеров.
        """
        conditions = [column == value for column, value in values]  # !! [] ?
        conditions = sa.or_(*conditions) if or_mode else sa.and_(*conditions)
        query = sa.select(User).join(Settings).where(conditions)

        return list((await self.session.scalars(query)).all())

    async def get_with_role(
        self,
        role: "Union[Roles, str]",
    ) -> list["User"]:
        """
        Возвращает всех пользователей, у которых есть роль.

        :param role: Роль.
        :return: Список юзеров.
        """
        if isinstance(role, Enum):
            role = role.value

        subquery = sa.select(Role.id).where(Role.role == role)
        query = (
            sa.select(User)
            .where(User.roles.any(sa.cast(subquery.as_scalar(), sa.Boolean)))
            .options(selectinload(User.roles))
        )

        return list((await self.session.scalars(query)).all())

    async def get_user_id_by_username(
        self,
        username: str,
    ) -> int | None:
        """
        Возвращает айди пользователя по его имени в базе.

        :param username: Имя юзера.
        :return: Айди юзера.
        """
        query = sa.select(User.user_id).where(User.username == username)
        return await self.session.scalar(query)

    async def save_new_to_db(
        self,
        user_id: int,
        username: str,
    ) -> None:
        """
        Сохраняет пользователя в базе данных, создаёт Settings и Laundry.

        Если пользователь уже существует, то обновляет статус ``is_active`` и никнейм,

        :param user_id: Айди юзера.
        :param username: Имя пользователя.
        """
        user = await self.get(user_id)

        # Если юзер в бд и (он помечен как неактивный или изменился никнейм)
        if user and (not user.is_active or user.username != username):
            user.is_active = True
            user.username = username
        elif not user:
            user = User(user_id=user_id, username=username)
            self.session.add(user)
            logger.info(f"Новый пользователь {user}")

        await self.session.commit()

    async def update(
        self,
        user_id: int,
        **fields: Any,
    ) -> None:
        """
        Обновление пользователя по айди.

        :param user_id: ТГ Айди юзера.
        :param fields: Поле таблицы=значение, ...
        """
        query = sa.update(User).where(User.user_id == user_id).values(**fields)
        await self.session.execute(query)
        await self.session.commit()

    async def is_has_any_role(
        self,
        user_id: int,
        roles: "list[Roles | str] | tuple[Roles| str, ...]",
    ) -> bool:
        """
        Имеет ли юзер хотя бы одну роль из переданных.

        :param user_id: ТГ Айди юзера.
        :param roles: Список ролей.
        :return: Тру или фэлс.
        """
        if (user := await self.get(user_id)) is None:
            return False

        role_names = [role.value if isinstance(role, Enum) else role for role in roles]
        return any(role.role in role_names for role in user.roles)
