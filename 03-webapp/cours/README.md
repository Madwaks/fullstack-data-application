# Développement d’Applications Web avec FastAPI et PostgreSQL
## Objectifs pédagogiques
- Comprendre l’architecture d’une application web moderne avec FastAPI.
- Savoir connecter FastAPI à une base de données relationnelle (PostgreSQL).
- Utiliser SQLAlchemy comme ORM pour modéliser des entités et gérer les relations.
- Implémenter un système complet de CRUD pour un blog avec Users et BlogPosts.
- Mettre en place les bonnes pratiques de structuration de projet (découpage en modules, dépendances, sécurité).

## 1. Architecture d’une application FastAPI + DB

Une application moderne suit une architecture en couches :
- API Layer (FastAPI endpoints) : reçoit les requêtes HTTP, gère la validation des données (via Pydantic).
- Service Layer : logique métier (gestion des utilisateurs, création d’articles, etc.).
- Data Layer : persistance des données avec SQLAlchemy.


- Database : PostgreSQL pour stocker les données relationnelles.

Avantage : séparation des responsabilités → plus facile à maintenir, tester et faire évoluer.

## 2. Mise en place du projet

### Installation des dépendances

pip install fastapi uvicorn[standard] psycopg2-binary sqlalchemy alembic python-dotenv

- fastapi : framework web asynchrone
- uvicorn : serveur ASGI
- sqlalchemy : ORM pour interagir avec PostgreSQL
- psycopg2-binary : driver PostgreSQL

## 2bis. Variables d'environnement et Docker Compose

Dans le développement d'applications, **les variables d'environnement** sont des paires clé/valeur accessibles par le système ou les processus. Elles permettent de stocker des informations de configuration qui peuvent changer selon l'environnement: mots de passe, clés secrètes, URL de base de données, etc.

**Pourquoi utiliser des variables d'environnement ?**
- Sécurité : évite de stocker des secrets (mots de passe, tokens) dans le code source.
- Flexibilité : permet de changer la configuration sans modifier le code.
- Portabilité : facilite le déploiement sur différents environnements (local, CI/CD, cloud...).

**Exemple de fichier `.env`** :
```
DATABASE_URL=postgresql://user:password@db:5432/blogdb
SECRET_KEY=supersecretkey
```

**Utilisation dans `docker-compose.yml`** :
Vous pouvez injecter ces variables dans vos conteneurs Docker via le paramètre `env_file` ou directement dans la section `environment` :
```yaml
services:
  api:
    build: .
    env_file:
      - .env
    # ou bien :
    # environment:
    #   - DATABASE_URL=postgresql://user:password@db:5432/blogdb
    #   - SECRET_KEY=supersecretkey
```

**Utilisation dans le code Python** :
Pour récupérer ces variables dans votre application (par exemple dans `database.py`), utilisez :
```python
import os
database_url = os.getenv("DATABASE_URL")
```

Cela permet à votre code d'être agnostique de l'environnement et de rester sécurisé.

## 3. Connexion à PostgreSQL

### database.py
```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/blogdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Le code ci-dessus établit la connexion à une instance PostgreSQL en suivant plusieurs étapes importantes :

1. **Configuration de l'URL de base de données** (ligne 41) : L'URL de connexion est récupérée depuis les variables d'environnement avec `os.getenv()`, permettant une configuration flexible selon l'environnement (développement, test, production). Le format `postgresql://user:password@localhost:5432/blogdb` suit la syntaxe standard PostgreSQL.

2. **Création du moteur SQLAlchemy** (ligne 43) : `create_engine()` initialise le moteur de base de données qui gère les connexions et les communications avec PostgreSQL.

3. **Configuration de la factory de sessions** (ligne 44) : `sessionmaker()` crée une classe de session configurée avec `autocommit=False` (gestion manuelle des transactions) et `autoflush=False` (contrôle explicite du flush).

4. **Classe de base pour les modèles** (ligne 46) : `declarative_base()` fournit la classe parente pour tous les modèles SQLAlchemy, gérant automatiquement les métadonnées et la création des tables.

5. **Gestionnaire de dépendance FastAPI** (lignes 52-57) : La fonction `get_db()` utilise le pattern de dépendance FastAPI avec `yield` pour :
   - Créer une nouvelle session de base de données pour chaque requête
   - Garantir la fermeture automatique de la session via le bloc `finally`
   - Permettre l'injection de dépendance dans les routes FastAPI

Ce pattern assure une gestion propre des connexions et évite les fuites de ressources.

## 4. Modélisation avec SQLAlchemy

### models.py
```

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    posts = relationship("BlogPost", back_populates="author")

class BlogPost(Base):
    __tablename__ = "blogposts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")

```

### Explication des modèles SQLAlchemy

Les modèles SQLAlchemy ci-dessus définissent la structure de notre base de données relationnelle en utilisant l'approche **Declarative Base** :

**Modèle User** :
- **`__tablename__`** : définit le nom de la table PostgreSQL ("users")
- **Colonnes** :
  - `id` : clé primaire auto-incrémentée avec index pour les performances
  - `first_name`, `last_name`, `email` : colonnes String avec contraintes (`nullable=False`, `unique=True`)
- **Relation** : `posts = relationship()` établit une relation One-to-Many avec BlogPost

**Modèle BlogPost** :
- **`__tablename__`** : table "blogposts"
- **Colonnes** :
  - `id` : clé primaire
  - `title` et `content` : données du post (String et Text pour contenu long)
  - `created_at` : timestamp automatique via `server_default=func.now()`
  - `author_id` : clé étrangère vers `users.id` avec `ForeignKey()`
- **Relation** : `author = relationship()` pour accéder à l'utilisateur propriétaire

**Relations bidirectionnelles** :
Le paramètre `back_populates` crée des relations bidirectionnelles :
- Depuis un User : `user.posts` → liste des BlogPost
- Depuis un BlogPost : `post.author` → objet User

SQLAlchemy se charge automatiquement de :
- Générer les requêtes SQL appropriées
- Maintenir l'intégrité référentielle
- Optimiser les jointures lors des requêtes

## 5. Serializers Pydantic (Validation des données)

### schemas.py



```
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class BlogPostBase(BaseModel):
    title: str
    content: str

class BlogPostCreate(BlogPostBase):
    pass

class BlogPost(BlogPostBase):
    id: int
    created_at: datetime
    author_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    posts: List[BlogPost] = []

    class Config:
        orm_mode = True
```

## 6. CRUD (Create, Read, Update, Delete)


``` crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# User CRUD
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

# BlogPost CRUD
def create_blogpost(db: Session, post: schemas.BlogPostCreate, user_id: int):
    db_post = models.BlogPost(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_blogposts(db: Session):
    return db.query(models.BlogPost).all()
```

Les fonctions CRUD ci-dessus implémentent les opérations de base pour manipuler les données en base :

**Principe CRUD** :
- **Create** : création de nouvelles entités
- **Read** : lecture/récupération des données
- **Update** : modification des entités existantes (non implémenté ici)
- **Delete** : suppression des entités (non implémenté ici)

**Fonctions User** :
- **`create_user()`** :
  - Convertit le schéma Pydantic en modèle SQLAlchemy avec `**user.dict()`
  - Ajoute l'objet à la session avec `db.add()`
  - Valide la transaction avec `db.commit()`
  - Actualise l'objet pour récupérer l'ID généré avec `db.refresh()`

- **`get_users()`** :
  - Utilise `db.query()` pour construire une requête SQLAlchemy
  - `.all()` récupère tous les enregistrements de la table

**Fonctions BlogPost** :
- **`create_blogpost()`** : même pattern que `create_user()` mais avec ajout du `author_id`
- **`get_blogposts()`** : récupère tous les posts (peut être optimisé avec jointures)

**Pattern de session** :
Toutes les fonctions reçoivent une `Session` SQLAlchemy en paramètre, permettant :
- La gestion des transactions (commit/rollback)
- L'isolation des opérations de base de données
- La réutilisation de la même session pour plusieurs opérations

Ce découpage permet une logique métier claire et testable, séparée des routes FastAPI.

## 7. Routes FastAPI

Une **route d’API** (ou endpoint) correspond à une URL spécifique exposée par votre serveur web qui permet aux clients (applications front-end, scripts, ou autres services) d’interagir avec votre application.  

Chaque route définit :  
- **Le chemin** : par exemple `/users/` ou `/posts/`.  
- **La méthode HTTP** : `GET`, `POST`, `PUT`, `DELETE`, etc., qui détermine le type d’opération (lecture, création, modification, suppression).  
- **La logique associée** : le code exécuté quand la route est appelée (souvent via des fonctions CRUD).  
- **La validation et sérialisation des données** : FastAPI utilise les **schémas Pydantic** pour vérifier les données reçues et formater les réponses automatiquement.  

En résumé, une route d’API est le point d’entrée par lequel le monde extérieur peut interagir avec votre application.


### routers/users.py
```
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db, user)

@router.get("/", response_model=list[schemas.User])
def read_users(db: Session = Depends(database.get_db)):
    return crud.get_users(db)
```

- **`APIRouter`** : crée un routeur modulaire avec préfixe `/users` et tag pour la documentation
- **Injection de dépendance** : `db: Session = Depends(database.get_db)` injecte automatiquement une session de base de données
- **Validation automatique** : `response_model=schemas.User` valide et sérialise la réponse selon le schéma Pydantic
- **Routes RESTful** :
  - `POST /users/` : création d'utilisateur avec validation du body via `schemas.UserCreate`
  - `GET /users/` : récupération de tous les utilisateurs avec sérialisation automatique

### routers/blogposts.py
```
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/posts", tags=["blogposts"])

@router.post("/", response_model=schemas.BlogPost)
def create_post(post: schemas.BlogPostCreate, db: Session = Depends(database.get_db)):
    return crud.create_blogpost(db, post, user_id=1)  # TODO: lier avec authentification

@router.get("/", response_model=list[schemas.BlogPost])
def read_posts(db: Session = Depends(database.get_db)):
    return crud.get_blogposts(db)
```

- **Structure identique** au router Users avec préfixe `/posts`
- **Limitation temporaire** : `user_id=1` en dur dans `create_post()` (à remplacer par authentification)
- **Pattern CRUD** : même approche avec injection de dépendance et validation Pydantic
- **Séparation des responsabilités** : le router ne fait que router vers les fonctions CRUD

📌 main.py
```
from fastapi import FastAPI
from .routers import users, blogposts
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(blogposts.router)
```

- **Création des tables** : `models.Base.metadata.create_all()` génère automatiquement les tables PostgreSQL au démarrage
- **Instance FastAPI** : `app = FastAPI()` crée l'application principale
- **Inclusion des routers** : `app.include_router()` monte les routers avec leurs préfixes respectifs
- **Architecture modulaire** : séparation claire entre routers, modèles et configuration de base de données
- **Auto-documentation** : FastAPI génère automatiquement la documentation OpenAPI/Swagger accessible via `/docs`

Cette structure permet une application scalable où chaque module a une responsabilité claire.
