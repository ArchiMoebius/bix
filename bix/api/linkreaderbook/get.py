import datetime
from typing import List

from fastapi import Depends, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from bix.api.linkreaderbook import router
from bix.database import get_session
from bix.model import Book, Reader, ReaderBookLink, ReaderResponse


class ReaderBookLinkResponse(BaseModel):
    id: int
    read_date: datetime.datetime
    read_self: bool
    read_aloud: bool
    book_id: int
    book_title: str
    book_image: str


class GetReaderBookResponse(BaseModel):
    results: List[ReaderBookLinkResponse]
    count: int


@router.get("/reader/{reader_id}/books", response_model=GetReaderBookResponse)
def _(
    *,
    session: Session = Depends(get_session),
    reader_id: int,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    base_query = select(ReaderBookLink).where(ReaderBookLink.reader_id == reader_id)
    query_results = session.exec(base_query.offset(offset).limit(limit)).all()
    results = []

    for readerbooklink in query_results:
        results.append(
            ReaderBookLinkResponse(
                id=readerbooklink.id,
                read_date=readerbooklink.read_date,
                read_self=readerbooklink.read_self,
                read_aloud=readerbooklink.read_aloud,
                book_id=readerbooklink.books.id,
                book_title=readerbooklink.books.title,
                book_image=readerbooklink.books.image,
            )
        )

    return GetReaderBookResponse(
        results=results,
        count=len(
            session.exec(base_query).all()
        ),  #  TODO: WHERE THE FUCK is `.count()` !!!
    )


class BookReaderLinkResponse(BaseModel):
    id: int
    read_date: datetime.datetime
    read_self: bool
    read_aloud: bool
    reader_id: int
    reader_name: str
    reader_age: int


class GetBookReaderResponse(BaseModel):
    results: List[BookReaderLinkResponse]
    count: int


@router.get("/book/{book_id}/readers", response_model=GetBookReaderResponse)
def _(
    *,
    session: Session = Depends(get_session),
    book_id: int,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    base_query = select(ReaderBookLink).where(ReaderBookLink.book_id == book_id)
    query_results = session.exec(base_query.offset(offset).limit(limit)).all()
    results = []

    for readerbooklink in query_results:
        results.append(
            BookReaderLinkResponse(
                id=readerbooklink.id,
                read_date=readerbooklink.read_date,
                read_self=readerbooklink.read_self,
                read_aloud=readerbooklink.read_aloud,
                reader_id=readerbooklink.readers.id,
                reader_name=readerbooklink.readers.name,
                reader_age=readerbooklink.readers.age,
            )
        )

    return GetBookReaderResponse(
        results=results,
        count=len(
            session.exec(base_query).all()
        ),  #  TODO: WHERE THE FUCK is `.count()` !!!
    )
