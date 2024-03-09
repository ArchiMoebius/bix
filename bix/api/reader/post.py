from fastapi import Depends
from sqlmodel import Session

from bix.api.reader import router
from bix.database import get_session
from bix.model import Reader, ReaderCreate


@router.post("/reader")
def _(
    *,
    session: Session = Depends(get_session),
    reader: ReaderCreate,
):
    db_reader = Reader.model_validate(reader)

    session.add(db_reader)
    session.commit()
    session.refresh(db_reader)

    return db_reader
