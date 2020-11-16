from typing import Optional, Union

from fastapi import Depends, HTTPException, status
from google.cloud.firestore_v1 import DocumentReference, DocumentSnapshot

from models import Command
from models.command_models import PatchCommand
from .fs_deps import fs_get_doc_snap, fs_get_doc_ref


async def fs_cmd_get_snap(name: str, game: Optional[int] = 0) -> DocumentSnapshot:
    return await fs_get_doc_snap(f"games/{game}/commands/{name}")


async def fs_snap_from_command(cmd: Command) -> DocumentSnapshot:
    return await fs_get_doc_snap(cmd.document_path)


async def fs_ref_from_command(cmd: Command) -> DocumentReference:
    return await fs_get_doc_ref(cmd.document_path)


async def fs_snap_exists(
    name: str,
    game: Optional[int] = 0,
    snap: DocumentSnapshot = Depends(fs_cmd_get_snap),
) -> DocumentSnapshot:
    """
    If the command doesn't exist this will raise a 404
    """
    if not snap.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Command '{name}' not found for game {game}.",
        )
    return snap


async def fs_snap_exists_from_cmd(
    cmd: Union[Command, PatchCommand]
) -> DocumentSnapshot:
    return await fs_snap_exists(cmd.name, cmd.game)
