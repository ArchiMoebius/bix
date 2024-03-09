import datetime
from typing import List

from fastapi import Depends, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from bix.api.linkcategorybook import router
from bix.database import get_session
from bix.model import Book, Category, CategoryBookLink, CategoryResponse


class CategoryBookLinkResponse(BaseModel):
    id: int
    category_name: str
    category_id: int
    book_id: int
    book_title: str
    book_image: str


class GetCategoryBookResponse(BaseModel):
    results: List[CategoryBookLinkResponse]
    count: int


@router.get("/category/{category_id}/books", response_model=GetCategoryBookResponse)
def _(
    *,
    session: Session = Depends(get_session),
    category_id: int,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    base_query = select(CategoryBookLink).where(
        CategoryBookLink.category_id == category_id
    )
    query_results = session.exec(base_query.offset(offset).limit(limit)).all()
    results = []

    for categorybooklink in query_results:
        results.append(
            CategoryBookLinkResponse(
                id=categorybooklink.id,
                category_name=categorybooklink.categories.name,
                category_id=categorybooklink.categories.id,
                book_id=categorybooklink.books.id,
                book_title=categorybooklink.books.title,
                book_image=categorybooklink.books.image,
            )
        )

    return GetCategoryBookResponse(
        results=results,
        count=len(
            session.exec(base_query).all()
        ),  #  TODO: WHERE THE FUCK is `.count()` !!!
    )


class BookCategoryLinkResponse(BaseModel):
    id: int
    category: str
    category_id: str


class GetBookCategoryResponse(BaseModel):
    results: List[BookCategoryLinkResponse]
    count: int


@router.get("/book/{book_id}/category", response_model=GetBookCategoryResponse)
def _(
    *,
    session: Session = Depends(get_session),
    book_id: int,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    base_query = select(CategoryBookLink).where(CategoryBookLink.book_id == book_id)
    query_results = session.exec(base_query.offset(offset).limit(limit)).all()
    results = []

    for readerbooklink in query_results:
        results.append(
            BookCategoryLinkResponse(
                id=readerbooklink.id,
                read_date=readerbooklink.read_date,
                read_self=readerbooklink.read_self,
                read_aloud=readerbooklink.read_aloud,
                reader_id=readerbooklink.readers.id,
                reader_name=readerbooklink.readers.name,
                reader_age=readerbooklink.readers.age,
            )
        )

    return GetBookCategoryResponse(
        results=results,
        count=len(
            session.exec(base_query).all()
        ),  #  TODO: WHERE THE FUCK is `.count()` !!!
    )
