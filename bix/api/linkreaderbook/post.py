from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from bix.api.linkreaderbook import router
from bix.database import get_session
from bix.model import Book, Reader, ReaderBookLink, ReaderBookLinkCreate


@router.post("/link/reader")
def _(*, session: Session = Depends(get_session), readerbooklink: ReaderBookLinkCreate):
    db_reader = session.get(Reader, readerbooklink.reader_id)

    if not db_reader:
        raise HTTPException(status_code=404, detail="reader not found")

    db_book = session.get(Book, readerbooklink.book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="book not found")

    db_reader_book_link = session.exec(
        select(ReaderBookLink)
        .where(ReaderBookLink.reader_id == readerbooklink.reader_id)
        .where(ReaderBookLink.book_id == readerbooklink.book_id)
    ).all()

    if len(db_reader_book_link) <= 0:
        session.add(
            ReaderBookLink(
                book_id=readerbooklink.book_id,
                reader_id=readerbooklink.reader_id,
                read_aloud=readerbooklink.read_aloud,
                read_self=readerbooklink.read_self,
            )
        )
    else:
        db_reader_book_link = db_reader_book_link[0]
        setattr(db_reader_book_link, "read_self", readerbooklink.read_self)
        setattr(db_reader_book_link, "read_aloud", readerbooklink.read_aloud)

        session.add(db_reader_book_link)

    session.commit()

    return {"ok": True}
