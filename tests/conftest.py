from contextlib import contextmanager
from unittest.mock import MagicMock

from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from google.cloud.firestore_v1 import DocumentSnapshot
from pytest import fixture

from main import app as _app

_client = TestClient(_app)


@fixture
def app() -> FastAPI:
    yield _app


@fixture
def client() -> TestClient:
    yield _client


@fixture
def dep_overrider(app):
    @contextmanager
    def wrapped(name, func):
        orig = app.dependency_overrides.copy()
        app.dependency_overrides[name] = func
        yield
        app.dependency_overrides = orig

    yield wrapped


@fixture
def raise_404_func():
    def ret_404():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    yield ret_404


@fixture
def raise_409_func():
    def ret_409():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    yield ret_409


@fixture
def mock_snap():
    mock = MagicMock(spec_set=DocumentSnapshot)
