#Структуры используемых баз данных
#////////////////////////////////////////////////////
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Date


class Base(DeclarativeBase):
    pass


class TaskBase(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_name: Mapped[str] = mapped_column(String(30))
    explain: Mapped[str] = mapped_column(String())
    creation_date: Mapped[str] = mapped_column(String())
    deadline: Mapped[str] = mapped_column(String())

    def __repr__(self) -> str:
        return f"TaskBase(id={self.id}, short_name={self.short_name}, explain={self.explain}, creation_date={self.creation_date}, deadline={self.deadline})"