from fastapi import APIRouter

router = APIRouter(tags=["category"])

from bix.api.category.delete import *
from bix.api.category.get import *
from bix.api.category.patch import *
from bix.api.category.post import *
