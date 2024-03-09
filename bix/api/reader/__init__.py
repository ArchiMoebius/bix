from fastapi import APIRouter

router = APIRouter(tags=["reader"])

from bix.api.reader.delete import *
from bix.api.reader.get import *
from bix.api.reader.patch import *
from bix.api.reader.post import *
