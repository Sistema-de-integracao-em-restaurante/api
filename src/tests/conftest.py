import pytest
from server import build_app
from alchemy_mock.mocking import UnifiedAlchemyMagicMock


@pytest.fixture()
def session_scope():
    session_scope = UnifiedAlchemyMagicMock()
    return session_scope


@pytest.fixture()
def app(session_scope):
    flask_app = build_app(session_scope)
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
