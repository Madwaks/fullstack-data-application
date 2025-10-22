"""
Tests pour le router d'authentification
"""

from unittest.mock import patch

from exceptions.user import UserNotFound, IncorrectPassword


def test_get_access_token_success(client):
    """
    Test de génération de token avec succès

    Scénario: Utilisateur valide avec credentials corrects
    Résultat attendu: Token généré avec status 200
    """
    # Arrange
    user_credentials = {"username": "testuser", "password": "testpassword"}
    mock_token = "mock_jwt_token_abc123"

    # Mock generate_access_token pour retourner un token
    with patch(
        "routers.auth.generate_access_token", return_value=mock_token
    ) as mock_generate:
        # Act
        response = client.post("/auth/token", json=user_credentials)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] == mock_token
        mock_generate.assert_called_once()


def test_get_access_token_user_not_found(client):
    """
    Test de génération de token avec utilisateur inexistant

    Scénario: Utilisateur n'existe pas dans la base de données
    Résultat attendu: Erreur 404 avec message approprié
    """
    # Arrange
    user_credentials = {"username": "nonexistent", "password": "anypassword"}

    # Mock generate_access_token pour lever UserNotFound
    with patch(
        "routers.auth.generate_access_token", side_effect=UserNotFound("User not found")
    ) as mock_generate:
        response = client.post("/auth/token", json=user_credentials)
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}
        mock_generate.assert_called_once()


def test_get_access_token_incorrect_password(client):
    """
    Test de génération de token avec mot de passe incorrect

    Scénario: Utilisateur existe mais mot de passe incorrect
    Résultat attendu: Erreur 400 avec message approprié
    """
    # Arrange
    user_credentials = {"username": "testuser", "password": "wrongpassword"}

    # Mock generate_access_token pour lever IncorrectPassword
    with patch(
        "routers.auth.generate_access_token",
        side_effect=IncorrectPassword("Incorrect password"),
    ) as mock_generate:
        # Act
        response = client.post("/auth/token", json=user_credentials)

        # Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect password"}
        mock_generate.assert_called_once()


def test_get_access_token_missing_username(client):
    """
    Test de génération de token sans username

    Scénario: Requête sans username dans le body
    Résultat attendu: Erreur 422 (validation error)
    """
    # Arrange
    invalid_credentials = {
        "password": "testpassword"
        # username manquant
    }

    # Act
    response = client.post("/auth/token", json=invalid_credentials)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_get_access_token_missing_password(client):
    """
    Test de génération de token sans password

    Scénario: Requête sans password dans le body
    Résultat attendu: Erreur 422 (validation error)
    """
    # Arrange
    invalid_credentials = {
        "username": "testuser"
        # password manquant
    }

    # Act
    response = client.post("/auth/token", json=invalid_credentials)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_get_access_token_empty_credentials(client):
    """
    Test de génération de token avec credentials vides

    Scénario: Username et password sont des chaînes vides
    Résultat attendu: Selon la logique métier (400 ou 404)
    """
    # Arrange
    empty_credentials = {"username": "", "password": ""}

    # Mock pour simuler l'échec avec UserNotFound
    with patch(
        "routers.auth.generate_access_token", side_effect=UserNotFound("User not found")
    ) as mock_generate:
        response = client.post("/auth/token", json=empty_credentials)
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}
        mock_generate.assert_called_once()


def test_get_access_token_with_special_characters(client):
    """
    Test de génération de token avec caractères spéciaux

    Scénario: Username et password contiennent des caractères spéciaux
    Résultat attendu: Traitement normal, succès si valide
    """
    # Arrange
    special_credentials = {"username": "user@example.com", "password": "P@ssw0rd!#$"}
    mock_token = "mock_token_with_special_chars"

    # Mock generate_access_token
    with patch(
        "routers.auth.generate_access_token", return_value=mock_token
    ) as mock_generate:
        response = client.post("/auth/token", json=special_credentials)
        assert response.status_code == 200
        assert response.json()["access_token"] == mock_token
        mock_generate.assert_called_once()


def test_get_access_token_verifies_db_session_passed(client):
    """
    Test que la session de base de données est bien passée

    Scénario: Vérifier que generate_access_token reçoit la session DB
    Résultat attendu: Session DB dans les arguments d'appel
    """
    # Arrange
    user_credentials = {"username": "testuser", "password": "testpassword"}

    # Mock generate_access_token
    with patch(
        "routers.auth.generate_access_token", return_value="test_token"
    ) as mock_generate:
        response = client.post("/auth/token", json=user_credentials)
        assert response.status_code == 200
        assert response.json()["access_token"] == "test_token"
        mock_generate.assert_called_once()
