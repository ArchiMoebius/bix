from fastapi import Depends, HTTPException
from sqlmodel import Session

from bix.api.book import router
from bix.database import get_session
from bix.model import Book


@router.delete("/book/{book_id}")
def _(*, session: Session = Depends(get_session), book_id: int):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(book)
    session.commit()

    return {"ok": True}
