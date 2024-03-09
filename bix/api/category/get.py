from typing import List

from fastapi import Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from bix.api.category import router
from bix.database import get_session
from bix.model import Category, CategoryRead


class GetCategoryResponse(BaseModel):
    results: List[CategoryRead]
    count: int


@router.get("/category/", response_model=GetCategoryResponse)
def _(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return GetCategoryResponse(
        results=session.exec(select(Category).offset(offset).limit(limit)).all(),
        count=len(
            session.exec(select(Category)).all()
        ),  #  TODO: WHERE THE FUCK is `.count()` !!!
    )


@router.get("/category/{category_id}", response_model=CategoryRead)
def _(
    *,
    session: Session = Depends(get_session),
    category_id: int,
):
    db_category = session.get(Category, category_id)

    if not db_category:
        raise HTTPException(status_code=404, detail="category not found")

    return db_category
