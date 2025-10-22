"""
Tests pour le router de posts - Route DELETE
"""

import pytest
import jwt
import os
from models import Post, User


@pytest.fixture
def auth_token(test_user):
    """Fixture pour générer un token JWT valide pour l'utilisateur de test"""
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "should-be-an-environment-variable")
    JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM", "HS256")
    return jwt.encode(
        {"user_id": str(test_user.id)},
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
    )


@pytest.fixture
def test_user_2(test_db_session):
    """Fixture pour un second utilisateur de test"""
    from services.auth import hash_password

    user = User(username="testuser2", password=hash_password("testpassword2"))
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    yield user
    test_db_session.delete(user)
    test_db_session.commit()


@pytest.fixture
def auth_token_user_2(test_user_2):
    """Fixture pour générer un token JWT valide pour le second utilisateur"""
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "should-be-an-environment-variable")
    JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM", "HS256")
    return jwt.encode(
        {"user_id": str(test_user_2.id)},
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
    )


@pytest.fixture
def test_post_for_user(test_db_session, test_user):
    """Fixture pour créer un post de test"""
    post = Post(
        title="Test Post", content="This is a test post", author_id=test_user.id
    )
    test_db_session.add(post)
    test_db_session.commit()
    test_db_session.refresh(post)
    post_id = post.id  # Store ID before yielding
    yield post
    # Cleanup: Check if post still exists before trying to delete
    existing_post = test_db_session.query(Post).filter(Post.id == post_id).first()
    if existing_post:
        test_db_session.delete(existing_post)
        test_db_session.commit()


def test_delete_post_success_as_author(
    client, test_db_session, test_user, auth_token, test_post_for_user
):
    """
    Test de suppression d'un post par son auteur avec succès

    Scénario: Utilisateur authentifié supprime son propre post
    Résultat attendu: Post supprimé avec status 200
    """
    # Arrange
    post_id = test_post_for_user.id

    # Act
    response = client.delete(
        f"/posts/{post_id}", headers={"Authorization": f"Bearer {auth_token}"}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(post_id)
    assert data["title"] == "Test Post"

    # Vérifier que le post a bien été supprimé de la base de données
    deleted_post = test_db_session.query(Post).filter(Post.id == post_id).first()
    assert deleted_post is None


def test_delete_post_unauthorized_no_token(client, test_post_for_user):
    """
    Test de suppression d'un post sans authentification

    Scénario: Tentative de suppression sans token d'authentification
    Résultat attendu: Erreur 422 (Validation Error - missing required header)
    """
    # Arrange
    post_id = test_post_for_user.id

    # Act - pas de header Authorization
    response = client.delete(f"/posts/{post_id}")

    # Assert - FastAPI retourne 422 pour les paramètres requis manquants
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_delete_post_unauthorized_invalid_token(client, test_post_for_user):
    """
    Test de suppression d'un post avec un token invalide

    Scénario: Tentative de suppression avec un token JWT invalide
    Résultat attendu: Erreur 401 (Unauthorized)
    """
    # Arrange
    post_id = test_post_for_user.id

    # Act
    response = client.delete(
        f"/posts/{post_id}", headers={"Authorization": "Bearer invalid_token"}
    )

    # Assert
    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"]


def test_delete_post_forbidden_wrong_author(
    client,
    test_db_session,
    test_user,
    test_user_2,
    auth_token_user_2,
    test_post_for_user,
):
    """
    Test de suppression d'un post par un utilisateur qui n'est pas l'auteur

    Scénario: Utilisateur authentifié tente de supprimer le post d'un autre utilisateur
    Résultat attendu: Erreur 403 (Forbidden)
    """
    # Arrange - test_post_for_user appartient à test_user, mais on utilise le token de test_user_2
    post_id = test_post_for_user.id

    # Act - utiliser le token d'un autre utilisateur
    response = client.delete(
        f"/posts/{post_id}", headers={"Authorization": f"Bearer {auth_token_user_2}"}
    )

    # Assert
    assert response.status_code == 403
    assert response.json() == {"detail": "Only author can delete their post"}


def test_delete_post_not_found(client, auth_token):
    """
    Test de suppression d'un post inexistant

    Scénario: Utilisateur authentifié tente de supprimer un post qui n'existe pas
    Résultat attendu: Erreur 404 (Not Found)
    """
    # Arrange
    post_id = "00000000-0000-0000-0000-000000000000"  # UUID qui n'existe pas

    # Act
    response = client.delete(
        f"/posts/{post_id}", headers={"Authorization": f"Bearer {auth_token}"}
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}


def test_delete_post_missing_bearer_prefix(client, test_post_for_user, auth_token):
    """
    Test de suppression avec header Authorization sans préfixe Bearer

    Scénario: Token fourni sans le préfixe "Bearer "
    Résultat attendu: Erreur 401 (Unauthorized)
    """
    # Arrange
    post_id = test_post_for_user.id

    # Act - token sans le préfixe "Bearer "
    response = client.delete(
        f"/posts/{post_id}",
        headers={"Authorization": auth_token},  # Sans "Bearer "
    )

    # Assert
    assert response.status_code == 401
    assert response.json() == {"detail": "No authorization header"}


def test_delete_post_verifies_authentication_before_deletion(
    client, test_db_session, test_user, auth_token, test_post_for_user
):
    """
    Test que l'authentification est vérifiée avant toute tentative de suppression

    Scénario: Vérifier que l'authentification est bien requise pour la suppression
    Résultat attendu: Avec authentification, le post est supprimé avec succès
    """
    # Arrange
    post_id = test_post_for_user.id

    # Act - avec un token valide
    response = client.delete(
        f"/posts/{post_id}", headers={"Authorization": f"Bearer {auth_token}"}
    )

    # Assert
    assert response.status_code == 200

    deleted_post = test_db_session.query(Post).filter(Post.id == post_id).first()
    assert deleted_post is None
