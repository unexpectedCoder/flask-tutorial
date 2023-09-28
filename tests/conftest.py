import os
import pytest as pt
import tempfile as tmp

from flaskr import create_app
from flaskr.db import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pt.fixture
def app():
    db_fd, db_path = tmp.mkstemp()
    app = create_app({
        "TESTING": True,
        "DATABASE": db_path
    })
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    
    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pt.fixture
def client(app):
    return app.test_client()


@pt.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client
    
    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login",
            data={"username": username, "password": password}
        )
    
    def logout(self):
        return self._client.get("/auth/logout")


@pt.fixture
def auth(client):
    return AuthActions(client)
