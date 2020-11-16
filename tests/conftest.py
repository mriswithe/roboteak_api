from contextlib import contextmanager
from unittest.mock import MagicMock

from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from google.cloud.firestore_v1 import DocumentSnapshot, AsyncDocumentReference
from pytest import fixture

from main import app as _app
from models import Command

_client = TestClient(_app)


@fixture(scope="session")
def app() -> FastAPI:
    yield _app


@fixture(scope="session")
def client() -> TestClient:
    yield _client


@fixture(scope="session")
def dep_overrider(app):
    @contextmanager
    def wrapped(name, func):
        orig = app.dependency_overrides.copy()
        app.dependency_overrides[name] = func
        yield
        app.dependency_overrides = orig

    yield wrapped


@fixture(scope="session")
def raise_404_func():
    def ret_404():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    yield ret_404


@fixture(scope="session")
def raise_409_func():
    def ret_409():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    yield ret_409


@fixture(scope="session")
def mock_cmd_factory():
    def make_mock_snap(cmd: Command) -> DocumentSnapshot:
        ref = AsyncDocumentReference(*cmd.document_path.split("/"))
        # noinspection PyTypeChecker
        snap = DocumentSnapshot(
            reference=ref,
            data=cmd.to_snap(),
            exists=True,
            read_time=None,
            create_time=None,
            update_time=None,
        )
        return snap

    yield make_mock_snap
