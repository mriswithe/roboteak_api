from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractModelInterface(ABC):
    model: BaseModel = BaseModel
    patch_model: BaseModel = BaseModel

    @abstractmethod
    async def get(self, name: str, game: int) -> model:
        pass

    @abstractmethod
    async def create(self, model: model):
        pass

    @abstractmethod
    async def update(self, name: str, game: int, model: model) -> patch_model:
        pass

    @abstractmethod
    async def delete(self, name: str, game: int):
        pass
