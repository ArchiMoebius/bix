from fastapi import Depends
from sqlmodel import Session

from bix.api.category import router
from bix.database import get_session
from bix.model import Category, CategoryCreate


@router.post("/category")
def _(
    *,
    session: Session = Depends(get_session),
    category: CategoryCreate,
):
    db_category = Category.model_validate(category)

    session.add(db_category)
    session.commit()
    session.refresh(db_category)

    return db_category
