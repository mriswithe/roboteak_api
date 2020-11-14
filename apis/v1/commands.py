from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from google.cloud.firestore_v1 import DocumentSnapshot

from models.command_models import Command, PatchCommand
from .deps.command_deps import fs_snap_exists, fs_snap_from_command

router = APIRouter()


@router.get("", response_model=Command)
async def get_command(
    snap: DocumentSnapshot = Depends(fs_snap_exists),
):
    return Command(name=snap.id, **snap.to_dict())


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Command)
async def create_command(
    cmd: Command, snap: DocumentSnapshot = Depends(fs_snap_from_command)
):
    if snap.exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Command '{cmd.name}' already exists for game {cmd.game}",
        )
    snap.reference.create(cmd.to_snap())
    snap = snap.reference.get()
    return Command.from_snap(snap)


@router.put("", response_model=Command)
async def update_command(
    patch_cmd: PatchCommand,
    name: str,
    game: Optional[int] = 0,
    snap: DocumentSnapshot = Depends(fs_snap_exists),
):
    if patch_cmd.name != name or patch_cmd.game != game:
        # TODO: Renaming/moving cmd to a new game
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot rename/regame an existing command. Feature coming.",
        )
    updated_command = Command.from_snap(snap).copy(
        update=patch_cmd.dict(exclude_unset=True, exclude_none=True)
    )
    snap.reference.update(updated_command.to_snap())
    return updated_command


@router.delete("")
async def delete_command(
    name: str,
    game: Optional[int] = 0,
    snap: DocumentSnapshot = Depends(fs_snap_exists),
):
    snap.reference.delete()
    return f"Command '{name}' for game {game} deleted."
