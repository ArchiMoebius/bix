from fastapi import APIRouter

router = APIRouter(tags=["category_book_link"])

from bix.api.linkcategorybook.delete import *
from bix.api.linkcategorybook.get import *
from bix.api.linkcategorybook.patch import *
from bix.api.linkcategorybook.post import *
