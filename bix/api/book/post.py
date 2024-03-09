from fastapi import Depends
from sqlmodel import Session

from bix.api.book import router
from bix.database import get_session
from bix.model import Book, BookCreate


@router.post("/book/")
def _(
    *,
    session: Session = Depends(get_session),
    book: BookCreate,
):
    db_book = Book.model_validate(book)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book
