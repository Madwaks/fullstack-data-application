from services.auth import (
    hash_password,
    check_password,
    generate_access_token,
    _encode_jwt,
    decode_jwt,
)
from exceptions.user import UserNotFound, IncorrectPassword
from serializers import User
from fastapi import HTTPException
import pytest


def test_hash_password():
    """Test de la fonction hash_password"""
    password = "testpassword"
    hashed_password = hash_password(password)

    assert hashed_password is not None
    assert isinstance(hashed_password, str)
    assert hashed_password != password


def test_check_password_correct():
    """Test que check_password retourne True avec le bon mot de passe"""
    password = "testpassword"
    hashed_password = hash_password(password)

    assert check_password(password, hashed_password) is True


def test_check_password_incorrect():
    """Test que check_password retourne False avec un mauvais mot de passe"""
    password = "testpassword"
    hashed_password = hash_password(password)

    assert check_password("wrongpassword", hashed_password) is False


def test_check_password_empty():
    """Test que check_password retourne False avec un mot de passe vide"""
    password = "testpassword"
    hashed_password = hash_password(password)

    assert check_password("", hashed_password) is False


def test_check_password_invalid_hash():
    """Test que check_password raise une erreur si le hash est invalide"""
    password = "testpassword"
    with pytest.raises(ValueError):
        check_password(password, "invalid_hash_format")


def test_generate_access_token(test_db_session, test_user):
    """Test que generate_access_token retourne un token JWT"""
    user_login = User(username="testuser", password="testpassword")
    token = generate_access_token(test_db_session, user_login)

    assert token is not None
    assert isinstance(token, str)


def test_generate_access_token_user_not_found(test_db_session):
    """Test que generate_access_token raise une erreur si l'utilisateur n'est pas trouvé"""
    user_login = User(username="wronguser", password="testpassword")
    with pytest.raises(UserNotFound):
        generate_access_token(test_db_session, user_login)


def test_generate_access_token_incorrect_password(test_db_session, test_user):
    """Test que generate_access_token raise une erreur si le mot de passe est incorrect"""
    user_login = User(username=test_user.username, password="wrongpassword")
    with pytest.raises(IncorrectPassword):
        generate_access_token(test_db_session, user_login)


def test_encode_jwt_correct(test_user):
    """Test que encode_jwt retourne un token JWT"""
    token = _encode_jwt(test_user)
    assert token is not None
    assert isinstance(token, str)


def test_decode_jwt_correct(test_user):
    """Test que decode_jwt retourne un utilisateur"""
    token = _encode_jwt(test_user)
    user = decode_jwt(token)
    assert user is not None
    assert isinstance(user, dict)
    assert user["user_id"] == str(test_user.id)


def test_decode_jwt_invalid_token(test_user):
    """Test que decode_jwt raise une erreur si le token est invalide"""
    token = "invalid_token"
    with pytest.raises(HTTPException) as err:
        decode_jwt(token)
    assert err.value.status_code == 401
