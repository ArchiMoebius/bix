"""from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from bix.database import get_session
from bix.model import BookCreate, Book, BookRead, BookUpdate
from bix.api.book import router


@router.patch("/book/{book_id}", response_model=BookRead)
def _(
    *,
    session: Session = Depends(get_session),
    book_id: int,
    book: BookUpdate,
):
    db_book = session.get(Book, book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = book.model_dump(exclude_unset=True)

    for key, value in book_data.items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book
"""
