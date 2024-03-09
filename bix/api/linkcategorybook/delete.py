"""from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from bix.database import get_session
from bix.model import BookCreate, Book, BookRead
from bix.api.book import router


@router.delete("/book/{book_id}")
def _(*, session: Session = Depends(get_session), book_id: int):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(book)
    session.commit()

    return {"ok": True}
"""
