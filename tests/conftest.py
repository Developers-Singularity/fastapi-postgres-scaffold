"""
Pytest fixtures for testing FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from src.database import Base, db_session
from sqlalchemy.orm import sessionmaker, Session
from src.main import create_app
from src.security import env_values

engine = create_engine(env_values["DB_TEST_URI"], pool_size=0, max_overflow=-1)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session() -> Session:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(session) -> TestClient:
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app = create_app()

    app.dependency_overrides[db_session] = override_get_db
    yield TestClient(app)


@pytest.fixture(scope="function")
def client_offline_db(session) -> TestClient:
    engine = create_engine(
        "postgresql://username:password@localhost:3000/nonexist",
        pool_size=0,
        max_overflow=-1,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # offline db session generator
    def override_get_db():       
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app = create_app()

    # override default engine session generator with offline db session generator
    app.dependency_overrides[db_session] = override_get_db
    yield TestClient(app)
