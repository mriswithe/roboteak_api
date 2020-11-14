from typing import Optional, Union

from fastapi import Depends, HTTPException, status
from google.cloud.firestore import CollectionReference
from google.cloud.firestore_v1 import DocumentSnapshot

from models import Command
from models.command_models import PatchCommand
from .fs_client import _COMMON_CLIENT


async def fs_cmd_game_col(game: Optional[int] = 0) -> CollectionReference:
    return _COMMON_CLIENT.collection(f"games/{game}/commands")


async def fs_cmd_get_snap(name: str, game: Optional[int] = 0) -> DocumentSnapshot:
    col_ref = await fs_cmd_game_col(game)
    snap = col_ref.document(name).get()
    return snap


async def fs_snap_from_command(cmd: Command) -> DocumentSnapshot:
    return await fs_cmd_get_snap(cmd.name, cmd.game)


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
