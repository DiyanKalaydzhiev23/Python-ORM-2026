from typing import Optional, List

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):  # equivalent of models.Model
    ...


class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    ingredients: Mapped[str] = mapped_column(Text)
    instructions: Mapped[str] = mapped_column(Text)
    chef_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chef.id"))
    chef: Mapped[Optional["Chef"]] = relationship(
        back_populates="recipes"
    )


class Chef(Base):
    __tablename__ = "chef"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    recipes: Mapped[List["Recipe"]] = relationship(
        back_populates="chef"
    )