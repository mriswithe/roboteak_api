from typing import Optional

from fastapi import Body, HTTPException, Query
from google.cloud.exceptions import Conflict, NotFound
from google.cloud.firestore_v1 import (
    AsyncDocumentReference,
    AsyncWriteBatch,
    DocumentSnapshot,
)
from starlette import status

from models.command_models import Command, PatchCommand
from .fs_client import _COMMON_CLIENT
from ..access_abc import AbstractModelInterface


class FBCommandInterface(AbstractModelInterface):
    model = Command
    patch_model = PatchCommand

    def __init__(self):
        self._client = _COMMON_CLIENT

    async def get(
        self, name: str = Query(...), game: Optional[int] = Query(0)
    ) -> model:
        return self.model.from_snap(await self._get_snap(name, game))

    async def create(self, new_model: model) -> model:
        ref = await self._get_ref(new_model.name, new_model.game)
        try:
            await ref.create(new_model.to_snap())
        except Conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Command '{new_model.name}' already exists for game {new_model.game}",
            ) from None
        return new_model

    async def update(
        self,
        name: str = Query(...),
        game: Optional[int] = Query(0),
        changes: patch_model = Body(...),
    ) -> model:
        snap = await self._get_snap(name, game)
        current_model = self.model.from_snap(snap)
        updated_model = current_model.copy(
            update=changes.dict(
                exclude_none=True, exclude_unset=True, exclude_defaults=True
            )
        )
        if (
            current_model.name != updated_model.name
            or current_model.game != updated_model.game
        ):
            # do the rename
            src_ref = await self._get_ref(name, game)
            dest_ref = await self._get_ref(updated_model.name, updated_model.game)
            await self._rename(src_ref, dest_ref, updated_model)
        else:
            await snap.reference.update(updated_model.to_snap())
        return await self.get(updated_model.name, updated_model.game)

    async def delete(self, name: str = Query(...), game: Optional[int] = Query(0)):
        await (await self._get_ref(name, game)).delete()

    async def _rename(
        self,
        src_ref: AsyncDocumentReference,
        dest_ref: AsyncDocumentReference,
        updated_model: model,
    ):
        batch: AsyncWriteBatch
        batch = self._client.batch()
        # noinspection PyTypeChecker
        batch.delete(src_ref)
        # noinspection PyTypeChecker
        batch.create(dest_ref, updated_model.to_snap())
        try:
            await batch.commit()
        except Conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Command '{dest_ref.id}' already exists for game "
                f"{updated_model.game}",
            )
        except NotFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Command '{src_ref.id}' does not exist for game "
                f"{src_ref.path.split('/')[1]}",
            )

    async def _get_snap(self, name: str, game: int) -> DocumentSnapshot:
        """
        Raises a 404 if the snap doesn't exist

        """
        ref = await self._get_ref(name, game)
        snap = await ref.get()
        if not snap.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Command '{name}' not found for game {game}.",
            )
        return snap

    async def _get_ref(self, name: str, game: int) -> AsyncDocumentReference:
        # noinspection PyTypeChecker
        return self._client.document(f"games/{game}/commands/{name}")
