from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from bix.api.category import router
from bix.database import get_session
from bix.model import Category, CategoryBookLink


@router.delete("/category/{category_id}")
def _(
    *,
    session: Session = Depends(get_session),
    category_id: int,
):
    category = session.get(Category, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="category not found")

    links = session.exec(
        select(CategoryBookLink).where(CategoryBookLink.category_id == category_id)
    ).all()

    for link in links:
        session.delete(link)

    session.delete(category)
    session.commit()

    return {"ok": True}
