from fastapi import APIRouter, Depends, status

from models.command_models import Command
from ..access_model.firebase_access.CommandInterface import FBCommandInterface

router = APIRouter()


command_interface = FBCommandInterface()


@router.get("", response_model=Command)
async def get_command(cmd: Command = Depends(command_interface.get)):
    return cmd


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Command)
async def create_command(cmd: Command = Depends(command_interface.create)):
    return cmd


@router.put("", response_model=Command)
async def update_command(cmd: Command = Depends(command_interface.update)):
    return cmd


@router.delete("", dependencies=(Depends(command_interface.delete),))
async def delete_command():
    pass
