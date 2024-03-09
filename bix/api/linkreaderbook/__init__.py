from fastapi import APIRouter

router = APIRouter(tags=["reader_book_link"])

from bix.api.linkreaderbook.delete import *
from bix.api.linkreaderbook.get import *
from bix.api.linkreaderbook.patch import *
from bix.api.linkreaderbook.post import *
