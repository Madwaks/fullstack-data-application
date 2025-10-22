## Introduction aux Tests Unitaires

### Définition et Objectifs

Les tests unitaires constituent la base de la pyramide de tests en développement logiciel. Un test unitaire est un test automatisé qui vérifie le comportement d'une unité de code isolée (généralement une fonction, une méthode ou une classe) dans un environnement contrôlé.

**Objectifs principaux :**
- Vérifier la conformité du code aux spécifications
- Détecter les régressions lors des modifications
- Faciliter la refactorisation en toute confiance
- Documenter le comportement attendu du code
- Améliorer la qualité et la maintenabilité

### Pyramide de Tests

```
    /\
   /  \     Tests E2E (End-to-End)
  /____\    - Peu nombreux, lents, coûteux
 /      \   
/________\  Tests d'Intégration
           - Nombre modéré, vitesse moyenne
           
Tests Unitaires
- Nombreux, rapides, peu coûteux
- Base de la pyramide
```

## Concepts Fondamentaux

### 1. AAA Pattern (Arrange, Act, Assert)

Le pattern AAA structure chaque test en trois phases distinctes :

```python
def test_calculate_total():
    # Arrange - Préparation des données de test
    items = [{"price": 10.0, "quantity": 2}, {"price": 5.0, "quantity": 3}]
    
    # Act - Exécution de la fonction à tester
    result = calculate_total(items)
    
    # Assert - Vérification du résultat
    assert result == 35.0
```

### 2. Fixtures et Setup/Teardown

Les fixtures permettent de configurer et nettoyer l'environnement de test. Elles utilisent le mécanisme `yield` pour séparer la phase de setup (avant yield) de la phase de teardown (après yield).

**Fixture simple :**
```python
@pytest.fixture
def sample_user():
    """Fixture pour créer un utilisateur de test"""
    return User(
        id=1,
        username="testuser",
        email="test@example.com"
    )

def test_user_creation(sample_user):
    assert sample_user.username == "testuser"
```

**Fixture avec base de données et nettoyage :**

Les fixtures avec `yield` permettent d'exécuter du code de nettoyage après le test :

```python
@pytest.fixture(scope="function")
def test_user(test_db_session, test_user_password, test_user_username):
    """
    Fixture pour créer un utilisateur dans la base de données
    
    1. Création de l'utilisateur
    2. Ajout à la session
    3. Commit pour persistance
    4. Refresh pour récupérer les données DB (ID auto-généré)
    5. Yield pour fournir l'utilisateur au test
    6. Delete et commit pour nettoyer après le test
    """
    # Setup : création de l'utilisateur
    user = User(
        username=test_user_username,
        password=hash_password(test_user_password)
    )
    test_db_session.add(user)
    test_db_session.commit()  # Persiste dans la DB
    test_db_session.refresh(user)  # Récupère les valeurs DB (ID, timestamps)
    
    # Le test s'exécute ici
    yield user
    
    # Teardown : nettoyage après le test
    test_db_session.delete(user)
    test_db_session.commit()
```

**Avantages du pattern yield :**
- **Isolation** : Chaque test repart avec une base propre
- **Nettoyage garanti** : Le code après `yield` s'exécute même si le test échoue
- **Gestion des ressources** : Fermeture de connexions, suppression de fichiers temporaires, etc.

### 3. Paramétrisation des Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

## Frameworks et Outils

### Pytest - Framework Principal

Pytest est le framework de test le plus populaire en Python pour sa simplicité et sa puissance.

**Installation :**
```bash
pip install pytest pytest-asyncio httpx
```

**Configuration (pytest.configure) :**

Au lieu d'utiliser un fichier `pytest.ini`, il est possible de configurer pytest directement dans le fichier `conftest.py` avec la fonction `pytest_configure()` :

```python
def pytest_configure(config):
    """
    Configuration dynamique de pytest
    Permet de configurer les marqueurs et autres options
    """
    config.addinivalue_line(
        "markers", "unit: Unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests"
    )
    config.addinivalue_line(
        "markers", "slow: Slow tests"
    )
```

Cette approche offre plus de flexibilité et permet de centraliser la configuration avec les fixtures.

### Outils Complémentaires

- **pytest-cov** : Couverture de code
- **pytest-mock** : Mocking avancé
- **pytest-xdist** : Tests parallèles
- **factory_boy** : Génération de données de test
- **faker** : Données factices réalistes

## Stratégies de Test

### 1. Test-Driven Development (TDD)

Le TDD suit le cycle Red-Green-Refactor :

1. **Red** : Écrire un test qui échoue
2. **Green** : Écrire le code minimal pour faire passer le test
3. **Refactor** : Améliorer le code en gardant les tests verts

### 2. Behavior-Driven Development (BDD)

Le BDD se concentre sur le comportement métier :

```python
def test_user_authentication():
    # Given - Un utilisateur valide existe
    user = create_user("test@example.com", "password123")
    
    # When - L'utilisateur tente de se connecter
    result = authenticate_user("test@example.com", "password123")
    
    # Then - L'authentification doit réussir
    assert result is not None
    assert result.email == "test@example.com"
```

### 3. Test Coverage

La couverture de code mesure le pourcentage de code exécuté par les tests. Pytest-cov offre plusieurs formats de rapport :

**Rapport en ligne de commande (term) :**
```bash
pytest --cov=app --cov-report=term
```

Ce rapport affiche directement dans le terminal :
- Le pourcentage de couverture par fichier
- Le nombre de lignes couvertes/manquantes
- Un résumé global

Exemple de sortie :
```
Name                          Stmts   Miss  Cover
-------------------------------------------------
app/__init__.py                   0      0   100%
app/services/auth.py             45      2    96%
app/routers/user.py              32      5    84%
-------------------------------------------------
TOTAL                           325     15    95%
```

**Rapport HTML interactif :**
```bash
pytest --cov=app --cov-report=html
```

Ce rapport génère un dossier `htmlcov/` avec une interface web interactive permettant de :
- Visualiser ligne par ligne le code couvert/non couvert
- Naviguer facilement entre les fichiers
- Identifier rapidement les zones non testées (lignes en rouge)
- Analyser les branches conditionnelles manquées

Pour consulter le rapport HTML :
```bash
open htmlcov/index.html  # macOS
# ou
xdg-open htmlcov/index.html  # Linux
# ou naviguer manuellement vers htmlcov/index.html dans un navigateur
```

**Combiner plusieurs rapports :**
```bash
pytest --cov=app --cov-report=term --cov-report=html
```

**Niveaux de couverture recommandés :**
- **Statements** : 80-90%
- **Branches** : 70-80%
- **Functions** : 90-95%
- **Lines** : 80-90%

**Options avancées :**
```bash
# Rapport avec détails des lignes manquantes
pytest --cov=app --cov-report=term-missing

# Définir un seuil minimum (échoue si < 80%)
pytest --cov=app --cov-fail-under=80

# Exclure certains fichiers avec .coveragerc
pytest --cov=app --cov-config=.coveragerc
```

## Mocking et Isolation

### 1. Mock Objects

Les mocks permettent d'isoler l'unité testée en remplaçant ses dépendances :

```python
from unittest.mock import Mock, patch

def test_user_service_with_mock():
    # Création d'un mock
    mock_database = Mock()
    mock_database.get_user.return_value = User(id=1, name="Test")
    
    # Injection du mock
    service = UserService(mock_database)
    result = service.get_user(1)
    
    # Vérification des interactions
    mock_database.get_user.assert_called_once_with(1)
    assert result.name == "Test"
```

### 2. Patching

Le patching permet de remplacer des fonctions ou des objets :

```python
@patch('services.auth.get_user_by_username')
def test_authenticate_user(mock_get_user):
    # Configuration du mock
    mock_get_user.return_value = User(username="test", password_hash="hash")
    
    # Test
    result = authenticate_user("test", "password")
    
    # Vérification
    mock_get_user.assert_called_once_with("test")
    assert result is not None
```

### 3. Spies et Stubs

- **Spy** : Enregistre les appels sans modifier le comportement
- **Stub** : Fournit des réponses prédéfinies
- **Mock** : Combine spy et stub avec vérifications

## Tests d'Intégration

### 1. Tests d'API

```python
from fastapi.testclient import TestClient

def test_create_post():
    client = TestClient(app)
    
    response = client.post(
        "/posts/",
        json={"title": "Test", "content": "Content"},
        headers={"Authorization": "Bearer token"}
    )
    
    assert response.status_code == 201
    assert response.json()["title"] == "Test"
```

### 2. Tests de Base de Données

Les tests de base de données utilisent les fixtures pour garantir l'isolation :

```python
def test_database_integration(test_db_session):
    """Test d'intégration avec la base de données
    
    La fixture test_db_session :
    1. Crée les tables avant le test
    2. Fournit une session propre
    3. Nettoie automatiquement après (yield pattern)
    """
    # Arrange
    user = User(username="testuser", email="test@example.com")
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    
    # Act
    retrieved = test_db_session.query(User).filter_by(id=user.id).first()
    
    # Assert
    assert retrieved is not None
    assert retrieved.email == "test@example.com"
    # Pas besoin de cleanup manuel, la fixture s'en charge


def test_user_creation_and_retrieval(test_db_session):
    """Test de création et récupération d'utilisateur"""
    # Create
    user = User(username="john", email="john@example.com")
    test_db_session.add(user)
    test_db_session.commit()
    
    # Retrieve
    found = test_db_session.query(User).filter_by(username="john").first()
    
    assert found.email == "john@example.com"
```

## Bonnes Pratiques

### 1. Nommage des Tests

```python
# Bon
def test_calculate_total_with_multiple_items():
    pass

def test_authenticate_user_with_valid_credentials():
    pass

# Éviter
def test_calc():
    pass

def test_auth():
    pass
```

### 2. Un Test, Une Assertion

```python
# Bon
def test_user_creation():
    user = create_user("test@example.com")
    assert user.email == "test@example.com"

def test_user_creation_sets_default_role():
    user = create_user("test@example.com")
    assert user.role == "user"

# Éviter
def test_user_creation():
    user = create_user("test@example.com")
    assert user.email == "test@example.com"
    assert user.role == "user"
    assert user.created_at is not None
```

### 3. Tests Indépendants

```python
# Chaque test doit être indépendant
def test_user_creation():
    user = create_user("test1@example.com")
    assert user.email == "test1@example.com"

def test_user_deletion():
    user = create_user("test2@example.com")
    delete_user(user.id)
    assert get_user(user.id) is None
```

### 4. Données de Test Réalistes

```python
# Utiliser des données réalistes
def test_email_validation():
    valid_emails = [
        "user@example.com",
        "test.user+tag@domain.co.uk",
        "user123@subdomain.example.org"
    ]
    
    for email in valid_emails:
        assert is_valid_email(email)
```

## Métriques et Qualité

### 1. Métriques de Couverture

La couverture de code peut être générée sous différents formats selon vos besoins :

```bash
# Couverture avec rapport terminal (par défaut)
pytest --cov=app

# Couverture avec rapport terminal détaillé (lignes manquantes)
pytest --cov=app --cov-report=term-missing

# Couverture avec rapport HTML interactif
pytest --cov=app --cov-report=html

# Combiner les deux rapports (terminal + HTML)
pytest --cov=app --cov-report=term --cov-report=html

# Couverture avec seuil minimum (échec si < 80%)
pytest --cov=app --cov-fail-under=80

# Configuration via .coveragerc pour exclure certains fichiers
pytest --cov=app --cov-config=.coveragerc
```

**Exemple de .coveragerc :**
```ini
[run]
omit = 
    */tests/*
    */venv/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
```

### 2. Métriques de Performance

```python
import time

def test_performance():
    start = time.time()
    result = expensive_operation()
    duration = time.time() - start
    
    assert result is not None
    assert duration < 1.0  # Doit s'exécuter en moins d'1 seconde
```

### 3. Mutation Testing

Le mutation testing évalue la qualité des tests en introduisant des bugs artificiels :

```bash
pip install mutmut
mutmut run
```

## Exemples Pratiques

### 1. Test d'un Service d'Authentification

Les tests sont organisés en **fonctions simples** plutôt qu'en classes. Chaque fonction de test est indépendante et utilise les fixtures pour le setup.

```python
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


def test_generate_access_token(test_db_session, test_user):
    """Test que generate_access_token retourne un token JWT
    
    Utilise les fixtures :
    - test_db_session : session de base de données de test
    - test_user : utilisateur créé automatiquement
    """
    user_login = User(username="testuser", password="testpassword")
    token = generate_access_token(test_db_session, user_login)

    assert token is not None
    assert isinstance(token, str)


def test_generate_access_token_user_not_found(test_db_session):
    """Test que generate_access_token raise une erreur si l'utilisateur n'existe pas"""
    user_login = User(username="wronguser", password="testpassword")
    
    with pytest.raises(UserNotFound):
        generate_access_token(test_db_session, user_login)


def test_generate_access_token_incorrect_password(test_db_session, test_user):
    """Test que generate_access_token raise une erreur avec mauvais mot de passe"""
    user_login = User(username=test_user.username, password="wrongpassword")
    
    with pytest.raises(IncorrectPassword):
        generate_access_token(test_db_session, user_login)
```

**Avantages des fonctions de test :**
- **Simplicité** : Moins de boilerplate que les classes
- **Lisibilité** : Chaque test est autonome et explicite
- **Fixtures** : Injection de dépendances automatique via les paramètres
- **Isolation** : Pas d'état partagé entre les tests comme avec `self`

### 2. Test d'un Router FastAPI

Les tests de routes utilisent le `TestClient` de FastAPI et peuvent être simplifiés avec des fonctions :

```python
def test_create_post_success(client, test_user, auth_headers):
    """Test de création d'un post avec succès
    
    Utilise les fixtures :
    - client : TestClient FastAPI
    - test_user : utilisateur de test
    - auth_headers : headers d'authentification
    """
    post_data = {
        "title": "New Post",
        "content": "This is a new post"
    }
    
    with patch('routers.post.get_current_user') as mock_get_user:
        mock_get_user.return_value = test_user
        
        response = client.post(
            "/posts/",
            json=post_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == post_data["title"]


def test_get_post_not_found(client, auth_headers):
    """Test de récupération d'un post inexistant"""
    response = client.get(
        "/posts/999",
        headers=auth_headers
    )
    
    assert response.status_code == 404


def test_create_post_unauthorized(client):
    """Test de création d'un post sans authentification"""
    post_data = {
        "title": "New Post",
        "content": "Content"
    }
    
    response = client.post("/posts/", json=post_data)
    
    assert response.status_code == 401
```

## Outils Avancés

### 1. Tests Asynchrones

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### 2. Tests Paramétrés Avancés

```python
@pytest.mark.parametrize("user_data,expected_status", [
    ({"username": "valid", "email": "valid@test.com"}, 201),
    ({"username": "", "email": "valid@test.com"}, 422),
    ({"username": "valid", "email": "invalid-email"}, 422),
])
def test_user_creation_validation(user_data, expected_status):
    response = client.post("/users/", json=user_data)
    assert response.status_code == expected_status
```

### 3. Fixtures Avancées

Les fixtures avec différents scopes permettent d'optimiser les performances des tests :

```python
@pytest.fixture(scope="session")
def test_db_engine():
    """
    Fixture de session pour l'engine de base de données
    Créée une seule fois pour toute la session de tests
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    return engine


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """
    Fixture pour la session de base de données
    Créée pour chaque test (scope="function")
    
    Le pattern yield garantit le nettoyage :
    1. Création des tables
    2. Création de la session
    3. Yield de la session au test
    4. Fermeture de la session
    5. Suppression des tables
    """
    from database import BaseSQL
    
    # Setup : création des tables
    BaseSQL.metadata.create_all(bind=test_db_engine)
    
    # Création de la session
    TestingSessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=test_db_engine
    )
    session = TestingSessionLocal()
    
    # Le test s'exécute ici
    yield session
    
    # Teardown : nettoyage garanti
    session.close()
    BaseSQL.metadata.drop_all(bind=test_db_engine)
```

**Scopes de fixtures :**
- `function` : Créée/détruite à chaque test (défaut)
- `class` : Partagée par tous les tests d'une classe
- `module` : Partagée par tous les tests d'un module
- `session` : Créée une seule fois pour toute la session

### 4. Tests de Charge

```python
import pytest
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def create_post(self):
        self.client.post("/posts/", json={
            "title": "Load Test Post",
            "content": "Content"
        })
```

## Conclusion

Les tests unitaires sont essentiels pour maintenir la qualité et la fiabilité du code. Ils permettent de :

- Détecter les bugs rapidement
- Faciliter la refactorisation
- Documenter le comportement attendu
- Améliorer la confiance dans le déploiement