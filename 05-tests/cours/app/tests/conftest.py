"""
Configuration globale pour pytest
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.auth import hash_password
from models import User


# Configuration des marqueurs pytest
def pytest_configure(config):
    pass


@pytest.fixture(scope="session")
def test_db_engine():
    engine = create_engine(
        os.getenv("DATABASE_URL"),
        pool_pre_ping=True,
    )
    return engine


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Fixture pour la session de base de données de test"""
    from database import BaseSQL

    # Crée toutes les tables
    BaseSQL.metadata.create_all(bind=test_db_engine)

    # Crée une session
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_db_engine
    )
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Supprime toutes les tables après chaque test
        BaseSQL.metadata.drop_all(bind=test_db_engine)


@pytest.fixture(scope="function")
def client():
    """Fixture pour TestClient"""
    from main import app

    return TestClient(app)


@pytest.fixture(scope="session")
def test_user_password():
    """Fixture pour le mot de passe de test"""
    return "testpassword"


@pytest.fixture(scope="session")
def test_user_username():
    """Fixture pour le nom d'utilisateur de test"""
    return "testuser"


@pytest.fixture(scope="function")
def test_user(test_db_session, test_user_password, test_user_username):
    """Fixture pour un utilisateur de test"""

    user = User(username=test_user_username, password=hash_password(test_user_password))
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)

    yield user

    test_db_session.delete(user)
    test_db_session.commit()
