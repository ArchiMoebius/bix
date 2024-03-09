from fastapi import Depends, HTTPException
from sqlmodel import Session

from bix.api.reader import router
from bix.database import get_session
from bix.model import Reader, ReaderRead, ReaderUpdate


@router.patch("/reader/{reader_id}", response_model=ReaderRead)
def _(
    *,
    session: Session = Depends(get_session),
    reader_id: int,
    reader: ReaderUpdate,
):
    db_reader = session.get(Reader, reader_id)

    if not db_reader:
        raise HTTPException(status_code=404, detail="reader not found")

    reader_data = reader.model_dump(exclude_unset=True)

    for key, value in reader_data.items():
        setattr(db_reader, key, value)

    session.add(db_reader)
    session.commit()
    session.refresh(db_reader)

    return db_reader
