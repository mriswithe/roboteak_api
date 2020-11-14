from fastapi import APIRouter
from . import commands

v1 = APIRouter()
v1.include_router(commands.router, prefix="/commands", tags=["commands"])
