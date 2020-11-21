from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel


class AbstractModelInterface(ABC):
    model: BaseModel = BaseModel
    patch_model: BaseModel = BaseModel

    @abstractmethod
    async def get(self, name: str, game: int) -> model:
        """
        get an instance of the model from the backend
        :param name: name of the model
        :param game: game of the model
        :return: model instance
        :raises: HTTPException 404 if command does not exist
        """
        pass

    @abstractmethod
    async def create(self, model: model) -> model:
        """
        Create a new model in the backend for provided model
        :param model: Instance of the model to be created
        :return: model: Interpret the model from the DB and return it, should match
        input model
        :raises: HTTPException 409 if command already exists
        """
        pass

    @abstractmethod
    async def update(self, name: str, game: int, changes: patch_model) -> model:
        """
        Update an existing model to match the specified params in `patch_model`
        :param name: name of the model
        :param game: game of the model
        :param changes: Instance of patch_model with only the updated attributes
        :return: Instance of the model as it exists after updates
        :raises: HTTPException 404 if model doesn't exist
            HTTPException 409 if renaming/changing game and the destination model
             name already exists
        """
        pass

    @abstractmethod
    async def delete(self, name: str, game: int) -> None:
        """
        Delete existing model, will succeed even if the intended model doesn't exist
        :param name: name of the model
        :param game: game of the model
        :return: None
        """
        pass

    @abstractmethod
    async def query_by_game(self, game: int, include_global=True) -> List[model]:
        """
        Return all of the models that match for the specified game, by default also
        return the "global" commands (game ID 0) unless otherwise specified
        :param game:
        :param include_global:
        :return:
        """
        pass
