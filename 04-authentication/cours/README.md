# Authentication

Dans cette section, nous allons voir comment mettre en place un système d'authentification basique avec FastAPI.
A partir d'un login classique avec username et mot de passe, nous allons générer un Token JWT (JSON Web Token)
qui sera ensuite utilisé pour s'authentifier sur nos endpoints qui seront configurés en conséquence.
Chaque endpoint qui attend une authentification acceptera un header `Authorization`. La valeur de ce header commencera par le mot `Bearer` suivi du token.

```
Authorization: Bearer <xxx>
```

## Informations de connexion d'un utilisateur

Dans la plupart des applications, des informations comme l'email et le mot de passe sont stockées pour permettre à un utilisateur d'accéder à son compte personnel.
Nous avons donc besoin d'ajouter des attributs à notre modèle `User` qui ne contient uniquement un nom et un prénom pour le moment.

```
username = Column(String, unique=True)
password = Column(String)
```

Pour des raisons de sécurité, nous n'allons pas écrire le mot de passe des utilisateurs en clair dans la base de données mais plutôt utiliser une technique de _hashing_
avant d'enregistrer les informations de l'utilisateur.

Une technique utilisée pour le stockage sécurisé de mot de passe par de nombreux services est `PBKDF2-HMAC-SHA256` (Django, AWS, ...).
C'est ce que nous allons implémenter ici.

C'est en fait une combinaison de techniques cryptographique:
- PBKDF2 → Password-Based Key Derivation Function 2
- HMAC   → Hash-based Message Authentication Code
- SHA256 → Secure Hash Algorithm 256-bit

La librairie standard de python nous offre la possibilité d'encoder des chaînes de caractères sans avoir à reinventer la roue.
Voici un exemple de fonction python nous permettant de générer une empreinte unique pour un mot de passe. C'est le résultat de cette fonction qui sera stockée en base.

```
import hashlib
import os
import base64
import hmac

def hash_password(password: str, iterations: int = 600_000) -> str:
    salt = os.urandom(16)

    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)

    salt_b64 = base64.b64encode(salt).decode('utf-8')
    hash_b64 = base64.b64encode(dk).decode('utf-8')

    return f"pbkdf2_sha256${iterations}${salt_b64}${hash_b64}"
```

Voici le résultat d'un hash de mot de passe : `pbkdf2_sha256$600000$auVU1ScNBWGDZ+6xQhdw1A==$KmW58rNsE3xirxyWFUX9jzgyPKC+ddnPRWXirb20T/0=`

Pour authentifier un utilisateur qui fournit son mot de passe qui lui n'est pas hashé, nous aurons besoin de comparer les hash obtenus avec les mots de passe. 

Voici un exemple de fonction en Python permettant de vérifier deux mots de passe dont l'un a déja été hashé.
```
import hashlib
import os
import base64
import hmac

def check_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt_b64, hash_b64 = stored_hash.split('$')
    except Exception:
        raise ValueError("Invalid hash format")

    iterations = int(iterations)
    salt = base64.b64decode(salt_b64)
    stored_dk = base64.b64decode(hash_b64)

    new_dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)

    return hmac.compare_digest(stored_dk, new_dk)
```


## JWT Token


Un JWT (JSON Web Token) est un moyen sécurisé d'échanger des informations entre deux parties.

Un tel token est constitué de trois parties : un header, un payload et une signature.

Le header contient des informations sur le type de token et l'algorithme de cryptage utilisé pour le signer (HMAC, RSA...).
Le payload contient les données que l'on veut transmettre (comme l'ID d'utilisateur, les rôles, etc.). Ces données peuvent être publiques ou privées.
Signature : C'est une sorte de vérification qui permet de s'assurer que le token n'a pas été modifié. Elle est créée en combinant le header, le payload et une clé secrète.

Voici un exemple de JWT Token

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibW9uX2lkIn0.qIBDak2Hk554hDP0hgHfMeQmt-D74kV21qQiHQ7AIow
```

Les trois parties distinctes sont séparées par un `.`.

## Encodage et décodage de JWT Token

Pour encoder un JWT Token, on utilise une librairie qui va nous permettre de générer un token à partir d'un payload et d'une clé secrète.

``` python
import jwt
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "should-be-an-environment-variable")
JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM", "HS256")

def _encode_jwt(user: User) -> str:
    return jwt.encode(
        {
            "user_id": "mon_id",
        },
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
    )
```

Il est fortement recommandé de stocker la clé secrète dans une variable d'environnement.

Pour décoder un JWT Token, on utilise la même librairie qui va nous permettre de vérifier la signature du token et de récupérer les données du payload.

``` python
def _decode_jwt(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_SECRET_ALGORITHM])
```

Ainsi, un tier ne possédant pas la clé secrète ne pourra pas vérifier la signature d'un token, en créer un ou en décoder un.

Par contre, un JWT Token en tant que tel est facilement décodable et lisible par n'importe qui.
En effet, il s'agit simplement d'une concaténation d'information encodée en base64.

Par exemple, on peut retrouver les informations encodées dans le token précédent en utilisant un décodeur en ligne (https://jwt.io/).

Lors de la création d'un token, on y associe généralement un temps d'expiration pour des raisons de sécurité.

## API endpoint avec authentification

Nous devons maintenant configurer nos endpoints pour recevoir un JWT Token, vérifier son intégrité et autoriser l'accès aux ressources.

Pour cela, nous allons utiliser une dépendance FastAPI qui va nous permettre de vérifier la validité du token.

```python
from fastapi.security import HTTPBearer

security=HTTPBearer()

@router.get("/{post_id}", dependencies=[Depends(security)], tags=["posts"])
async def get_post_by_id(post_id: str, request: Request, db: Session = Depends(models.get_db)):
    auth_header  = request.headers.get("Authorization")

    token = verify_autorization_header(auth_header)

    post = posts_service.get_post_by_id(post_id=post_id, db=db)

    if str(post.user_id) != token.get("user_id"):
        raise HTTPException(status_code=403, detail=f"Forbidden {post.user_id} {token.get('user_id')}")

    return post
```

Pour une simple authentification, FastAPI nous fournit une dépendance `HTTPBearer` qui va nous permettre de vérifier la présence d'un token dans le header `Authorization`.
Vous verrez apparaitre un petit cadenas à côté de l'endpoint pour indiquer qu'il est sécurisé.

![img.png](img.png)

Pour s'authentifier, il suffit de générer un token et de l'envoyer dans le header `Authorization` de la requête HTTP.
La documentation de l'API vous offre un bouton pour tester l'endpoint avec un token.
En cliquant sur le cadenas, vous verrez une fenêtre s'ouvrir pour vous permettre de rentrer un token.

![img_1.png](img_1.png)

Il nous faut désormais décoder ce token pour vérifier l'identité de l'utilisateur.
Voici un exemple de fonction qui va nous permettre de vérifier le token.

```python
def verify_autorization_header(access_token: str):
    if not access_token or not access_token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No auth provided.")

    try:
        token = access_token.split("Bearer ")[1]
        auth = jwt.decode(
            token, JWT_SECRET_KEY, JWT_SECRET_ALGORITHM
        )
    except jwt.InvalidTokenError as err:
        raise HTTPException(status_code=401, detail=f"Invalid token.")

    return auth
```

Ainsi, nous avons mis en place un système d'authentification basique avec FastAPI. 
Toutes les requêtes vers les endpoints sécurisés devront être accompagnées d'un token valide. Sinon la requete sera rejetée
