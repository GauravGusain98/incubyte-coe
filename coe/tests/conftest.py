import os
os.environ["ENV"] = "test"

import pytest
from fastapi.testclient import TestClient
from alembic.config import Config
from alembic import command

from coe.db.session import get_db
from coe.db.session import engine, SessionLocal as TestingSessionLocal
from main import app

@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("script_location", "alembic")
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


@pytest.fixture(scope="function")
def db(request):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Use marker to determine whether to rollback
    should_rollback = request.node.get_closest_marker("rollback") is not None

    try:
        yield session
    finally:
        session.close()
        if should_rollback:
            transaction.rollback()
        else:
            transaction.commit()
        connection.close()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
