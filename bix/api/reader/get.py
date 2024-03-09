from typing import List

from fastapi import Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from bix.api.reader import router
from bix.database import get_session
from bix.model import Reader, ReaderRead


class GetReaderResponse(BaseModel):
    results: List[ReaderRead]
    count: int


@router.get("/reader/", response_model=GetReaderResponse)
def _(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return GetReaderResponse(
        results=[
            reader.calculate_age()
            for reader in session.exec(select(Reader).offset(offset).limit(limit)).all()
        ],
        count=len(
            session.exec(select(Reader)).all()
        ),  #  TODO: WHERE THE FUCK is `.count()` !!!
    )


@router.get("/reader/{reader_id}", response_model=ReaderRead)
def _(
    *,
    session: Session = Depends(get_session),
    reader_id: int,
):
    db_reader = session.get(Reader, reader_id)

    if not db_reader:
        raise HTTPException(status_code=404, detail="reader not found")

    return db_reader.calculate_age()
