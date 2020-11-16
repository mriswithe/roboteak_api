from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app as _app
from pytest import fixture
from contextlib import contextmanager


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
