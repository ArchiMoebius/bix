import datetime
from datetime import date
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

# ****************** START CATEGORY ***************


class CategoryBookLinkBase(SQLModel):
    book_id: Optional[int] = Field(
        default=None,
        foreign_key="book.id",
        nullable=False,
        index=True,
    )
    category_id: Optional[int] = Field(
        default=None,
        foreign_key="category.id",
        nullable=False,
        index=True,
    )


class CategoryBookLink(CategoryBookLinkBase, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        nullable=False,
        index=True,
    )
    categories: "Category" = Relationship(back_populates="books")
    books: "Book" = Relationship(back_populates="categories")


class CategoryBookLinkCreate(CategoryBookLinkBase):
    pass


class CategoryBase(SQLModel):
    name: str = Field(index=True, nullable=False, regex="[-a-zA-Z0-9]{3,32}")


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        nullable=False,
    )
    books: List[CategoryBookLink] = Relationship(
        back_populates="categories",
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class CategoryUpdate(CategoryBase):
    id: int


class CategoryResponse(CategoryBase):
    id: int


# ****************** END CATEGORY *****************

# ****************** START LINK *******************


class ReaderBookLinkBase(SQLModel):
    book_id: Optional[int] = Field(
        default=None,
        foreign_key="book.id",
        nullable=False,
        index=True,
    )
    reader_id: Optional[int] = Field(
        default=None,
        foreign_key="reader.id",
        nullable=False,
        index=True,
    )


class ReaderBookLink(ReaderBookLinkBase, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        nullable=False,
        index=True,
    )
    read_date: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
    )
    read_self: bool
    read_aloud: bool
    readers: "Reader" = Relationship(back_populates="books")
    books: "Book" = Relationship(back_populates="readers")


class ReaderBookLinkCreate(ReaderBookLinkBase):
    read_self: bool
    read_aloud: bool


class ReaderBookLinkRead(ReaderBookLinkBase):
    pass


class ReaderBookLinkUpdate(ReaderBookLinkBase):
    pass


# ****************** END LINK *********************


# ****************** START BOOK *******************


class BookBase(SQLModel):
    title: str = Field(index=True)
    author: str = Field(index=True)
    description: str = Field(index=True)
    publisher: str = Field(index=True)
    publish_date: str = Field(nullable=False)
    isbn10: Optional[str] = Field(
        title="ISBN Number",
        description="A number used to track books",
        index=True,
        regex="[0-9]+",
        nullable=True,
    )
    isbn13: Optional[str] = Field(
        title="ISBN Number",
        description="A number used to track books",
        index=True,
        regex="[0-9]+",
        nullable=True,
    )
    image: Optional[str]
    lexile: Optional[str]


class Book(BookBase, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        nullable=False,
    )

    readers: List[ReaderBookLink] = Relationship(
        back_populates="books",
    )
    categories: List[CategoryBookLink] = Relationship(
        back_populates="books",
    )


class BookResponse(BookBase):
    id: int


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int


class BookUpdate(BookBase):
    pass


# ****************** END BOOK *********************


# ****************** START READER *****************
class ReaderBase(SQLModel):
    name: str = Field(index=True, nullable=False)
    birthdate: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
    )
    age: int = 0

    def __init__(self):
        self.calculate_age()

    def calculate_age(self):
        today = date.today()

        self.age = (
            today.year
            - self.birthdate.year
            - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        )

        return self


class Reader(ReaderBase, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        nullable=False,
    )

    books: List[ReaderBookLink] = Relationship(
        back_populates="readers",
    )


class ReaderResponse(ReaderBase):
    id: int


class ReaderCreate(ReaderBase):
    pass


class ReaderRead(ReaderBase):
    id: int
    age: int


class ReaderUpdate(ReaderBase):
    pass
