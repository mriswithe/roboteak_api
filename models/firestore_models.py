from abc import ABC, abstractmethod


class FirestoreMixin(ABC):
    @property
    @abstractmethod
    def collection_path(self):
        ...

    @property
    @abstractmethod
    def document_path(self):
        ...
