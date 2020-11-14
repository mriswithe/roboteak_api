from datetime import datetime
from functools import partial
from threading import Event, Lock
from typing import Any, List, Optional, Union
from collections import defaultdict

from google.cloud.firestore import Client, DocumentSnapshot
from google.cloud.firestore_v1 import CollectionReference, DocumentReference, Query
from google.cloud.firestore_v1.watch import DocumentChange, ChangeType
from pydantic import ValidationError
from pydantic.generics import GenericModel

from twitch_models import ChatCommand


class OldFirestoreWatcher:
    game_commands_template = "commands/{game_id}/commands/"

    def __init__(self, client: Optional[Client] = None):
        self._watchers = {}
        self._collections = defaultdict(dict)
        if client is None:
            self._client = Client()
        else:
            self._client = client
        self._watchers_lock = Lock()

    def __del__(self):
        for colname, watcher in self._watchers:
            watcher.unsubscribe()

    def _watch_new_collection(self, collection):
        with self._watchers_lock:
            if collection not in self._watchers:
                col_ref = self._client.collection(collection)
                col_cb = partial(self._collection_callback, collection=collection)
                self._watchers[collection] = col_ref.on_snapshot(col_cb)

    # noinspection PyUnusedLocal
    def _collection_callback(
        self,
        docs: List[DocumentSnapshot],
        changes: List[DocumentChange],
        read_time: datetime,
        collection: str,
    ):
        col_dict = self._collections[collection]

        for change in changes:
            if change.type in [ChangeType.ADDED, ChangeType.MODIFIED]:
                try:
                    chat_command = ChatCommand(**change.document.to_dict())
                except ValidationError:
                    print(f"Error parsing change for doc {change.document.id}")
                    continue
                col_dict[change.document.id] = chat_command
            elif change.type == ChangeType.REMOVED:
                col_dict.pop(change.document.id)

    def get_cmd(self, cmd_name: str, game_id: int = "global"):
        pass

    def get_cmds_for_game(self, collection: Optional[int]):
        pass


class FirestoreWatcher:
    def __init__(
        self,
        target: Union[CollectionReference, DocumentReference, Query],
        model: Optional[Any] = None,
    ):
        self._target = target
        self._data = {}
        self._model = model
        self._watcher = target.on_snapshot(self._cb)

        self.changed = Event()

    # noinspection PyUnusedLocal
    def _cb(
        self,
        docs: List[DocumentSnapshot],
        changes: List[DocumentChange],
        read_time: datetime,
    ):
        for change in changes:
            if change.type in [ChangeType.ADDED, ChangeType.MODIFIED]:
                if self._model:
                    try:
                        result = self._model(**change.document.to_dict())
                        result = self._model()
                    except ValidationError:
                        print(f"Error parsing change for doc {change.document.id}")
                        continue
                else:
                    result = change.document.to_dict()
                self._data[change.document.id] = result
            elif change.type == ChangeType.REMOVED:
                self._data.pop(change.document.id)
        self.changed.set()

    @property
    def data(self):
        return self._data

    @property
    def target(self):
        return self._target
