from sqlalchemy import Column, Date, ForeignKey, Integer, String

from src.database.models.base_model import BaseModel


class Menu(BaseModel):
    __tablename__ = 'menus'

    id = Column(
        Integer,
        primary_key=True, autoincrement=True,
        unique=True, nullable=False
    )

    date = Column(
        Date,
        unique=True, nullable=False, index=True
    )

    edit_by = Column(Integer, ForeignKey('users.id'), default=0)

    breakfast = Column(String)
    lunch = Column(String)
    dinner = Column(String)
    snack = Column(String)
    supper = Column(String)

    def __repr__(self):
        return self._repr(
            id=self.id,
            date=self.date,
            breakfast=self.breakfast,
            lunch=self.lunch,
            dinner=self.dinner,
            snack=self.snack,
            supper=self.supper
        )
