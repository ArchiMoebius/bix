from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from bix.api.linkcategorybook import router
from bix.database import get_session
from bix.model import Book, Category, CategoryBookLink, CategoryBookLinkCreate


@router.post("/link/category")
def _(
    *, session: Session = Depends(get_session), categorybooklink: CategoryBookLinkCreate
):
    db_category = session.get(Category, categorybooklink.category_id)

    if not db_category:
        raise HTTPException(status_code=404, detail="category not found")

    db_book = session.get(Book, categorybooklink.book_id)

    if not db_book:
        raise HTTPException(status_code=404, detail="book not found")

    db_category_book_link = session.exec(
        select(CategoryBookLink)
        .where(CategoryBookLink.category_id == categorybooklink.category_id)
        .where(CategoryBookLink.book_id == categorybooklink.book_id)
    ).all()

    if len(db_category_book_link) <= 0:
        session.add(
            CategoryBookLink(
                book_id=categorybooklink.book_id,
                category_id=categorybooklink.category_id,
            )
        )

    session.commit()

    return {"ok": True}
