from fastapi import Depends, HTTPException
from sqlmodel import Session

from bix.api.category import router
from bix.database import get_session
from bix.model import Category, CategoryRead, CategoryUpdate


@router.patch("/category/{category_id}", response_model=CategoryRead)
def _(
    *,
    session: Session = Depends(get_session),
    reader_id: int,
    category: CategoryUpdate,
):
    db_category = session.get(Category, reader_id)

    if not db_category:
        raise HTTPException(status_code=404, detail="category not found")

    category_data = category.model_dump(exclude_unset=True)

    for key, value in category_data.items():
        setattr(db_category, key, value)

    session.add(db_category)
    session.commit()
    session.refresh(db_category)

    return db_category
