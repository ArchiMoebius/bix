from typing import List, Optional

from fastapi import Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, column, select

from bix.api.book import router
from bix.common.googleapi import searchBookByISBN
from bix.database import get_session
from bix.model import Book, BookRead


class GetBookResponse(BaseModel):
    results: List[BookRead]
    count: int


class GetBookSearchResponse(BaseModel):
    title: str
    description: str
    author: str
    publisher: str
    publish_date: str
    isbn10: int
    isbn13: int
    image: bytes
    lexile: str


@router.get("/book/", response_model=GetBookResponse)
def _(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: Optional[str],
):
    statement = select(Book).offset(offset).limit(limit)

    if search and len(search) > 2:
        # statement = statement.where(Book.title.regexp_match('^(b|c)'))
        statement = statement.filter(column("title").contains(search))

    return GetBookResponse(
        results=session.exec(statement).all(),
        count=len(
            session.exec(select(Book)).all()
        ),  #  TODO: WHERE THE FUCK is `.count()` !!!
    )


@router.get("/book/id/{book_id}", response_model=BookRead)
def _(
    *,
    session: Session = Depends(get_session),
    book_id: int,
):
    db_book = session.get(Book, book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="book not found")

    return db_book


@router.get("/book/isbn/{isbn}", response_model=GetBookSearchResponse)
def _(
    *,
    session: Session = Depends(get_session),
    isbn: str,
):
    googleAPIdata = searchBookByISBN(isbn)

    if not googleAPIdata:
        raise HTTPException(status_code=404, detail="Book not found")

    return GetBookSearchResponse(**googleAPIdata)
