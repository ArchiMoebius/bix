from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from bix.api.reader import router
from bix.database import get_session
from bix.model import Reader, ReaderBookLink


@router.delete("/reader/{reader_id}")
def _(*, session: Session = Depends(get_session), reader_id: int):
    reader = session.get(Reader, reader_id)

    if not reader:
        raise HTTPException(status_code=404, detail="reader not found")

    links = session.exec(
        select(ReaderBookLink).where(ReaderBookLink.reader_id == reader_id)
    ).all()

    for link in links:
        session.delete(link)

    session.delete(reader)
    session.commit()

    return {"ok": True}
