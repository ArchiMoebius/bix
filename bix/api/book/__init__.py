from fastapi import APIRouter

router = APIRouter(tags=["book"])

from bix.api.book.delete import *
from bix.api.book.get import *
from bix.api.book.patch import *
from bix.api.book.post import *
